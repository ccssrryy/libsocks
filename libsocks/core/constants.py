# o  X'00' NO AUTHENTICATION REQUIRED
# o  X'01' GSSAPI
# o  X'02' USERNAME/PASSWORD
# o  X'03' to X'7F' IANA ASSIGNED
# o  X'80' to X'FE' RESERVED FOR PRIVATE METHODS
# o  X'FF' NO ACCEPTABLE METHODS

METHOD_NO_AUTH = 0
METHOD_GSSAPI = 1
METHOD_USERNAME_PASSWORD = 2
METHOD_NO_ACCEPT = 0xFF

# o  VER    protocol version: X'05'
# o  REP    Reply field:
#    o  X'00' succeeded
#    o  X'01' general SOCKS server failure
#    o  X'02' connection not allowed by ruleset
#    o  X'03' Network unreachable
#    o  X'04' Host unreachable
#    o  X'05' Connection refused
#    o  X'06' TTL expired
#    o  X'07' Command not supported
#    o  X'08' Address type not supported
#    o  X'09' to X'FF' unassigned
# o  RSV    RESERVED
# o  ATYP   address type of following address
#    o  IP V4 address: X'01'
#    o  DOMAINNAME: X'03'
#    o  IP V6 address: X'04'

VER5 = 5
VER4 = 4
REP_SUCCEED = 0
REP_FAILURE = 1
REP_NOT_ALLOWED = 2
REP_NETWORK_UNREACHABLE = 3
REP_HOST_UNREACHABLE = 4
REP_CONNECTION_REFUSED = 5
REP_TTL_EXPIRED = 6
REP_CMD_NOT_SUPPORT = 7
REP_ADDR_NOT_SUPPORT = 8

RSV = 0

ATYP_IPV4 = 1
ATYP_DOMAINNAME = 3
ATYP_IPV6 = 4

# o  CMD
#     o  CONNECT X'01'
#     o  BIND X'02'
#     o  UDP ASSOCIATE X'03'

CMD_CONNECT = 1
CMD_BIND = 2
CMD_UDP_ASSOCIATE = 3


# socks4

# VN is the version of the reply code and should be 0. CD is the result
# code with one of the following values:
#
# 	90: request granted
# 	91: request rejected or failed
# 	92: request rejected becasue SOCKS server cannot connect to
# 	    identd on the client
# 	93: request rejected because the client program and identd
# 	    report different user-ids.

CD_GRANTED = 90
CD_REJECTED = 91
CD_CANNOT_CONNECT = 92
CD_DIFF_UIDS = 93
