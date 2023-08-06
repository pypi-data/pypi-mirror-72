import struct
from python_perl_storable.exception import PerlStorableException
from python_perl_storable.constants import *
from data_printer import p, np


def is_ref(obj):
    return isinstance(obj, (dict, list, tuple)) \
        or isinstance(obj, object) and hasattr(obj, '__dict__')


class StorableWriter:
    def __init__(self, iconv):
        self.hseen = {}
        self.tagnum = -1
        self.hclass = {}
        self.classnum = 0
        self.storable = [] # выходной буфер
        self.iconv = iconv
    
    def writeUInt8(self, number):
        self.storable.append( struct.pack("B", number) )
    
    def writeInt32LE(self, number):
        self.storable.append( struct.pack("<i", number) )
    
    def writeInt32BE(self, number):
        self.storable.append( struct.pack(">i", number) )
    
    def writeInt8(self, number):
        self.storable.append( struct.pack("b", number) )
    
    def writeInt64LE(self, number):
        self.storable.append( struct.pack("<q", number) )
    
    def writeDouble64LE(self, number):
        self.storable.append( struct.pack("<d", number) )

    def write(self, string):
        self.storable.append(string)

    def magic_write(self):
        self.writeUInt8(STORABLE_BIN_MAJOR << 1)
        self.writeUInt8(STORABLE_BIN_MINOR)
        # sizeof the array includes the 0 byte at the end:
        self.writeUInt8(len(BYTEORDER_BYTES))
        self.write(BYTEORDER_BYTES)
        self.writeInt8(SIZE_OF_INT)
        self.writeInt8(SIZE_OF_LONG)
        self.writeInt8(SIZE_OF_CHAR_PTR)
        self.writeInt8(SIZE_OF_NV)

    def save_scalar(self, sv):
        if len(sv) < 256:
            self.writeUInt8(SX_SCALAR)
            self.writeUInt8(len(sv))
        else:
            self.writeUInt8(SX_LSCALAR)
            self.writeInt32LE(len(sv))
        self.write(sv)

    def hv_store(self, sv):
        self.hseen[id(sv)] = self.tagnum


    def store(self, sv, from_ref=False):

        if id(sv) in self.hseen:
            if is_ref(sv):
                self.writeUInt8(SX_REF)
                self.tagnum += 1
            self.writeUInt8(SX_OBJECT)
            self.writeInt32BE(self.hseen[id(sv)])
            return

        self.tagnum += 1

        if sv is None:
            self.writeUInt8(SX_UNDEF)
        elif isinstance(sv, str):
            self.hv_store(sv)

            if self.iconv:
                self.save_scalar(self.iconv(sv))
            else:
                sv = sv.encode('utf-8')
                if is_ascii(sv):
                    self.save_scalar(sv)
                else:
                    if len(sv) < 256:
                        self.writeUInt8(SX_UTF8STR)
                        self.writeUInt8(len(sv))
                    else:
                        self.writeUInt8(SX_LUTF8STR)
                        self.writeInt32LE(len(sv))
                    self.write(sv)
        elif isinstance(sv, bytes):
            self.hv_store(sv)
            self.save_scalar(sv)
        elif isinstance(sv, int):
            if -128 <= sv < 128:
                self.writeUInt8(SX_BYTE)
                self.writeUInt8(sv+128)
            else:
                self.writeUInt8(SX_INTEGER)
                self.writeInt64LE(sv)
        elif isinstance(sv, float):
            self.hv_store(sv)
            self.writeUInt8(SX_DOUBLE)
            self.writeDouble64LE(sv)
        elif isinstance(sv, object) and hasattr(sv, '__dict__'):
            self.hv_store(sv)
            name = sv.__class__.__name__.replace("__", "::")
            if name in self.hclass:
                self.writeUInt8(SX_IX_BLESS)
                classnum = self.hclass[name]
                if classnum <= LG_BLESS:
                    self.writeUInt8(classnum)
                else:
                    self.writeUInt8(0x80)
                    self.writeInt32LE(classnum)
            else:
                self.classnum += 1
                self.hclass[name] = self.classnum
                self.writeUInt8(SX_BLESS)
                if len(name) <= LG_BLESS:
                    self.writeUInt8(len(name))
                else:
                    self.writeUInt8(0x80)
                    self.writeInt32LE(len(name))
                self.write(bytes(name, 'utf-8'))
            #self.tagnum -= 1
            if isinstance(sv, (list, tuple)):
                self.store(list(sv), True)
            else:
                self.store(sv.__dict__, True)
        elif isinstance(sv, (list, tuple)):
            if not from_ref:
               self.writeUInt8(SX_REF) 
               self.tagnum += 1
            self.hv_store(sv)
            self.writeUInt8(SX_ARRAY)
            self.writeInt32LE(len(sv))
            for i in sv: 
                self.store(i)
        elif isinstance(sv, dict):
            if not from_ref:
               self.writeUInt8(SX_REF)
               self.tagnum += 1
            self.hv_store(sv)
            self.writeUInt8(SX_HASH)
            self.writeInt32LE(len(sv))
            for i in sv:
                self.store(sv[i])
                key = bytes(i, 'utf-8')
                self.writeInt32LE(len(key))
                self.write(key)

        else:
            raise PerlStorableException('Undefined type `%s`' % (type(sv),))

        
        
    def ref_store(self, sv):
        self.magic_write()
        self.store(sv, from_ref=True)


class StorableWriterDebug(StorableWriter):

    def writeUInt8(self, number):
        self.debug("writeUInt8", number, 1)
        super.writeUInt8(number)
    
    def writeInt32LE(self, number):
        self.debug("writeInt32", number)
        super.writeInt32LE(number)
    
    def writeInt32BE(self, number):
        self.debug("writeInt32", number)
        super.writeInt32BE(number)
    
    def writeInt8(self, number):
        self.debug("writeInt8", number)
        super.writeInt8(number)
    
    def writeInt64LE(self, number):
        self.debug("writeInt64", number)
        super.writeInt64LE(number)
    
    def writeDouble64LE(self, number):
        self.debug("writeDouble", number)
        super.writeDouble64LE(number)

    def write(self, string):
        print("write %s" % string)
        super.write(string)

    def store(self, sv, from_ref=False):
        print("/-- store id=%s from_ref=%s" % (self.hseen[id(sv)] if id(sv) in self.hseen else 'no', from_ref) )
        p(sv)
        super.store(sv, from_ref)
        print(" --/")

def freeze(sv, iconv=None, magic=False, debug=False):
    w = StorableWriterDebug(iconv=iconv) if debug else StorableWriter(iconv=iconv)
    w.ref_store(sv)
    return b''.join(([MAGICSTR_BYTES] if magic else []) + w.storable)

