"""
This script uploads ldiff (import file for user's account)
to OpenLDAP using python API wrapper.
"""

from StringIO import StringIO
import ldif
import ldap
from ldap import modlist

# Open a connection
l = ldap.initialize("ldaps://ldap.company.com:636/")

# Bind/authenticate with a user with apropriate rights to add objects
l.simple_bind_s("cn=admin,dc=company,dc=com","'E8$[}q]pass83")

# The dn of our new entry/object
dn="cn=vpupkin,cn=people,ou=Company,dc=company,dc=com" 


ldif_file = StringIO("""dn: cn=vpupkin,cn=people,ou=Company,dc=company,dc=com
c: UA
cn: vpupkin
employeetype: Indoor Front-end developer
gidnumber: 500
givenname: Vasya
homedirectory: /home/vpupkin
host: example.com
l: Kyiv
loginshell: /bin/bash
mail: vpupkin@company.com
o: Company
objectclass: inetOrgPerson
objectclass: posixAccount
objectclass: top
objectclass: shadowAccount
objectclass: ldapPublicKey
objectclass: extensibleObject
labeleduri: skype://bruce
sn: Pupkin
sshpublickey: ssh-rsa key
st: Brucewillivskaya, 15
telephonenumber: 7777777777
uid: vpupkin
uidnumber: 1222
userpassword: {SHA}fEqNCco3Yq9h5ZUglD3CZJT4lBs=
""")

parser = ldif.LDIFRecordList(ldif_file)
parser.parse()

#print(parser.all_records)

for dn, entry in parser.all_records:
    add_modlist = modlist.addModlist(entry)
    l.add_s(dn, add_modlist)

