import sys
import struct

WAV_HEADER_SIZE = 2000

#from aplay/formats.h
'''
#define WAV_FMT_PCM             0x0001
#define WAV_FMT_IEEE_FLOAT      0x0003
#define WAV_FMT_DOLBY_AC3_SPDIF 0x0092
#define WAV_FMT_EXTENSIBLE 0xfffe
'''
PCM = 0x0001
IEEE_FLOAT = 0x0003
DOLBY_AC3_SPDIF = 0x0092
EXTENSIBLE = 0xfffe
#aplay doesnt even know about these
#from http://www-mmsp.ece.mcgill.ca/Documents/AudioFormats/WAVE/WAVE.html
ALAW = 0x0006
MULAW = 0x0007

def get_fmt_type(fmt_type):
	return {
		PCM : "PCM",
		IEEE_FLOAT : "IEEE_FLOAT",
		DOLBY_AC3_SPDIF : "DOLBY_AC3_SPDIF",
		EXTENSIBLE : "EXTENSIBLE",
		ALAW : "ALAW",
		MULAW : "MULAW" 
	}.get(fmt_type, "UNKNOWN")

wav_file = sys.argv[1]
print(wav_file)

fd = open(wav_file, 'rb')
header = fd.read(WAV_HEADER_SIZE)
fd.close()

riff = header[0:4].decode('ascii')
if riff != "RIFF":
	print("not a wav file. exiting...")
	exit(-1)

print("file type: "+riff)

file_size = struct.unpack("i", header[4:8])[0]
print("file size: "+str(file_size)) #always 8 bytes less than actual size

wave = header[8:12].decode('ascii')
print("sub file type: "+wave)

fmt = header[12:16].decode('ascii')
print("fmt marker: "+fmt)

fmt_data_length = struct.unpack("i", header[16:20])[0]
print("fmt data length: "+str(fmt_data_length))

format_type = struct.unpack("H", header[20:22])[0]
print("fmt type: "+hex(format_type))
print("fmt type as text: "+get_fmt_type(format_type))

num_channels = struct.unpack("h", header[22:24])[0]
print("number of channels: "+str(num_channels))

sample_rate = struct.unpack("i", header[24:28])[0]
print("sample rate: "+str(sample_rate))

sample_rate_bits_channels = struct.unpack("i", header[28:32])[0]
print("(sample rate * bits/sample *channels )/8: "+str(sample_rate_bits_channels))

bits_per_sample_channels = struct.unpack("h", header[32:34])[0]
print("bits/sample * channels: "+str(bits_per_sample_channels))

bits_per_sample = struct.unpack("h", header[34:36])[0]
print("bits per sample: "+str(bits_per_sample))

extra_param_size = 0
if format_type == EXTENSIBLE:
	extra_param_size = struct.unpack("h", header[36:38])[0]
	print("extra param size: "+str(extra_param_size))
	extra_param_size += 2

	extra_bits_per_sample = struct.unpack("H", header[38:40])[0]
	print("extra valid bits per sample: "+str(extra_bits_per_sample))

	extra_channel_mask = struct.unpack("i", header[40:44])[0]
	print("extra channel mask: "+str(extra_channel_mask))

	#so this is just long winded way of telling us its PCM
	#i couldnt find any docs saying that there was a compression format in use
	#but i suppose RIFF/WAV supports it
	extra_guid_fmt = struct.unpack("H", header[44:46])[0]
	print("extra guid format: "+str(extra_guid_fmt)+" "+get_fmt_type(extra_guid_fmt))

	extra_guid = header[46:60]#14 bytes
	print( ''.join('{:02x}'.format(x) for x in extra_guid))



index = 36 + extra_param_size

chunk_header = '' 
while chunk_header != "data":
	chunk_header = header[index:index+4].decode('ascii')
	print(chunk_header)
	chunk_size = struct.unpack("i", header[index+4:index+8])[0]
	print("chunk "+chunk_header+" length: "+str(chunk_size))
	index += 8 +chunk_size
'''
list_ = header[60:64].decode('ascii')
print(list_)

next_header = struct.unpack("i", header[64:68])[0]
print("list len: "+str(next_header))

head_ = header[68+next_header:68+next_header+4].decode('ascii')
print(head_)

data_length = struct.unpack("i", header[68+next_header+4:68+next_header+8])[0]
print("data length: "+str(data_length))	
'''

'''	
is_data_chunk = False
index = 16 + fmt_data_length + extra_param_size
while not is_data_chunk:
	chunk_header = header[index:index+4].decode('ascii')
	print("chunk header: "+chunk_header)

	chunk_length = struct.unpack("H", header[index+4:index+6])[0]

	if chunk_header == "data":
		is_data_chunk = True
		print("data size: "+str(chunk_length))
	else:
		print("chunk size: "+str(chunk_length))

	index = index + 4 + chunk_length

'''


'''	
data_start = 16+fmt_data_length+extra_param_size#36+extra_param_size
data = header[data_start:data_start+4].decode('ascii')
print("data header: "+data)

data_size = struct.unpack("i", header[data_start+4:data_start+8])[0]
print("data size: "+str(data_size))
'''

	



