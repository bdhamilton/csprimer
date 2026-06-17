# TCP SYN Flood

Goal: determine which percentage of incoming SYN messages captured in the file were ACKed.

The idea here is that (1) I get some more practice working with binary data, and (2) I see that network data often comes binary-encoded, not just in strings.

* A [SYN flood](https://en.wikipedia.org/wiki/SYN_flood) is where an attacker floods a listening TCP server with `SYN` requests and then never acknowledges their response, intending to leave them in an overloaded state.
* `file synflood.pcap` shows: `pcap capture file, microsecond ts (little-endian) - version 2.4 (No link-layer encapsulation, capture length 262144)`. 
* `man pcap-savefile` shows that a pcap contains a 24-byte header that includes its snapshot length, followed by packets, each of which have their on 16-byte header that includes its timestamp and the length of the packet, followed by the contents of the packet itself.
  * Initial observation: I should be able to figure out how many total packets are in the file by, skipping the file header, looking at each per-packet header for the length and skipping ahead to find the next header.
* `f.read(number_of_bytes)` will consume the requested amount of the file, and leave the rest of the file available for later use. So we can peel off just the per-file header with `f.read(24)`.
* `struct.unpack()` no longer [feels like magic](../varint/README.md). The first argument takes a declarative code that says (1) whether the data should be read as LE or BE (`<` or `>`) and (2) a series of [format characters](https://docs.python.org/3/library/struct.html#format-characters) that explains how to break down the binary data. The second argument takes a list of bytes that needs to match the length of the data the format characters attempt to parse. 
  * For example: In the case of the per-packet header, `struct.unpack('<IHHIIII', f.read(24))` means to read off a 24-byte header, read it in little-endian format, and decompose it into one int (4 bytes), two half-ints (2 bytes each), and then four more ints.
* After each per-packet header starts there is a _link layer header_. Its [type](https://www.tcpdump.org/linktypes.html) is declared at the end of the per-file header. (It's not entirely clear to me whehter this should be treated as part of the packet or if this is an artifact of the pcap savefile format.)
  * In this case, the link layer is `LINKTYPE_NULL`, because all the packets are coming over localhost. The corresponding header is [four octets](https://www.tcpdump.org/linktypes/LINKTYPE_NULL.html) that describes the protocol type, in this case IPv4.
* **All network byte order is big-endian.** That means that even though the pcap file is little-endian in my case, the header length describes lengths in big-endian format.
* The IPv4 packet [also has a header + payload structure](https://en.wikipedia.org/wiki/IPv4#Packet_structure). The second half of the first octet describes the "internet header length," which we can read to skip down to the next section.
* To isolate just a part of a byte (a `nibble`), we can use a mask. In this case: `packet[4] & 0x0f` or `0b00001111` sets the first four bits to 0 so we just have a four-bit number.
* After the IPv4 header comes the TCP header, which also has [a defined header structure](https://en.wikipedia.org/wiki/Transmission_Control_Protocol#TCP_segment_structure) that includes a number of single-bit flags you can set, including `SYN` and `ACK`.
* To see how many `SYN`s are getting `ACK`ed, we can just keep count of the number of the packets each flag flipped. 
  * In the context of this exercise, we expect essentially all packets to include SYN, since both the requests coming in and the initial ACK going back have a SYN, but ACKs to trail behind, because the client is nevering ACKing.