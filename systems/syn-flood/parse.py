import struct

with open("synflood.pcap", "rb") as f:
    magic_number, major, minor, _, _, _, llh_type = struct.unpack('<IHHIIII', f.read(24))

    assert magic_number == 0xa1b2c3d4
    assert major == 2
    assert minor == 4
    assert llh_type == 0 # localhost

    packets = 0
    ack_count = 0
    syn_count = 0

    while True:
        # Stop when there are no more packets to read.
        per_packet_header = f.read(16)
        if len(per_packet_header) == 0: 
            break

        # Keep a count.
        packets += 1

        # Pull apart the header and the packet.
        _, _, length, untruncated_length = struct.unpack('<IIII', per_packet_header)

        packet = f.read(length)

        # Constrain the program: we're not handle truncated packets,
        # and we're only handling IPv4 (type 2)
        assert length == untruncated_length
        assert struct.unpack('<I', packet[:4])[0] == 2

        # First layer: IPv4 header
        internet_header_length = (packet[4] & 0x0f) * 4 # drop first four bits and convert 'words' to bytes
        assert internet_header_length == 20 # bytes---no options

        # Second layer: TCP header
        tcp_header = packet[4 + internet_header_length:4 + internet_header_length + 20]
        flags = tcp_header[13]
        ack_set = flags & 0b00010000 == 0b00010000
        syn_set = flags & 0b00000010 == 0b00000010
        if ack_set:
            ack_count += 1
        if syn_set:
            syn_count +=1
        

    print(f"Total packets found: { packets }")
    print(f"{ack_count} packets included ack ({ ack_count / packets * 100}%)")
    print(f"{syn_count} packets included syn ({ syn_count / packets * 100}%)")