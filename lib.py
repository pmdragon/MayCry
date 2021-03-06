#!/usr/bin/python

from Crypto.Hash import SHA256
from Crypto.Cipher import AES

charUseless=' ' #blank space

class Text(object):
    """docstring for Text."""
    _blocks=[]
    def __init__(self):
        super(Text, self).__init__()
        self.refresh()

    def addBlock(self,block):
        self._blocks.append(block)

    def refresh(self):
        self._blocks=[]

    def getBlocks(self):
        return self._blocks

    def setBlocks(self,b):
        self._blocks=b

    def __str__(self):
        tmp=""
        for b in self.getBlocks():
            tmp+=b
        return tmp+"|"


class PlainText(Text):
    """docstring for PlainText."""

    def __init__(self, arg=None, sizeBlock=None):
        super(PlainText, self).__init__()
        if (arg is not None) and (sizeBlock is not None):
            self.arg = arg
            self.sizeBlock=sizeBlock
            self._splitForSizeBlock()
        else:
            self.refresh()

    def _splitForSizeBlock(self):
        self.arg+=(self.sizeBlock-(len(self.arg)%self.sizeBlock))*charUseless
        self.setBlocks([self.arg[i: i + self.sizeBlock] for i in range(0, len(self.arg), self.sizeBlock)])


class CypherText(Text):
    """docstring for CypherText."""
    def __init__(self):
        super(CypherText, self).__init__()


class Crypto(object):
    """docstring for Crypto."""
    SIZE_BLOCK=16

    def __init__(self, obj, password):
        super(Crypto, self).__init__()
        self.obj = obj
        self.encrypter= AES.new('This is a key123', AES.MODE_ECB)
        self.plain = PlainText(obj, self.SIZE_BLOCK)
        self.cypher =CypherText()
        self.textDecrypt = PlainText()
        self._encrypt()
        self._decrypt()

    def _encrypt(self):
        self.cypher.refresh()
        for block in self.plain.getBlocks():
            self.cypher.addBlock(self.encrypter.encrypt(block))

    def _decrypt(self):
        self.textDecrypt.refresh()
        for block in self.cypher.getBlocks():
            self.textDecrypt.addBlock(self.encrypter.decrypt(block))

    def __str__(self):
        view="PlainText:  "+ str(self.plain)+"\n"
        view+="CypherText: "+ str(self.cypher)+"\n"
        view+="DecrytText: "+ str(self.textDecrypt)

        return view
