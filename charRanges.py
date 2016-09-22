# Unicode character ranges for languages using Myanmar script

import sys

# From the Unicode Myanmar block, Extended-A, and Extended-B.

class langCodes:
  def __init__(self, name, range_list):
    self.name = name
    self.raw_range = range_list

  def expand(self):
    # Take the list of ranges and create a full list of characters.
    self.fullList = []
    for x in self.raw_range:
      if isinstance(x, list):
        first = x[0]
        last = x[1]
        for y in xrange(first, last+1):
          self.fullList.append(y)
      else:
        # A single value
        self.fullList.append(x)

  def numCodes(self):
    return len(self.fullList)


# These are language-specific ranges, but other characters in the Myanmar script are used
burmeseCodes = langCodes('Burmese', [[0x1000, 0x1021], [0x1023, 0x103e], [0x1040, 0x104f]])  # Fix

monCodes = langCodes('Mon', [0x1028, [0x1033, 0x1035], [0x105a, 0x1060]])
paliSanskritCodes = langCodes('Pali & Sanskrit', [[0x1050, 0x1059]])
shanCodes = langCodes('Shan', [[0x1075, 0x108d], [0x1090, 0x1099], [0x109e, 0x109f]])

sgawKarenCodes = langCodes("S'gwa Karen", [[0x1061, 0x1064]])
westernPhoKarenCodes = langCodes('Western Pho Karen', [[0x1065, 0x106D]])
easternPhoKarenCodes = langCodes('Eastern Pho Karen', [[0x106e, 0x1070]])
gebaKarenCodes = langCodes('Geba Karen', [0x1071])

kayahCodes = langCodes('Kayah', [[0x1072, 0x1074]])

rumaiPalaungCodes = langCodes('Rumai Palaung', [[0x108e, 0x108f]])

khantiShanCodes = langCodes('Khanti Shan', [[0x109a, 0x109b], [0xaa60, 0xaa73], [0xaa74, 0xaa76]])

aitonPhakenCodes = langCodes('Aiton & Phaken', [[0x109c, 0x109d], [0xaa77, 0xaa7a]])

paoKarenCodes = langCodes("Pa'o Karen", [0xaa7b])

taiLaingCodes = langCodes('Tai Liang', [[0xaa7c, 0xaa7d], [0xa9e7, 0xa9fe], [0xa9f0, 0xa9f9]])

shwePalaungCodes = langCodes('Shwe Palaung', [[0xaa7e, 0xaa7f]])

shanPaliCodes = langCodes('Shan Pali', [[0xa9e0, 0xa9e5], 0xa9e6])

codeList = [burmeseCodes, monCodes, paliSanskritCodes, shanCodes, sgawKarenCodes,
    westernPhoKarenCodes, easternPhoKarenCodes, gebaKarenCodes, kayahCodes,
    rumaiPalaungCodes, khantiShanCodes, aitonPhakenCodes, paoKarenCodes, 
    taiLaingCodes, shwePalaungCodes, shanPaliCodes]
    
# Non-standard areas typical for non-Unicode
nonStd = langCodes('nonStd', [0x1022, 0x1026, 0x1028, 0x102a, 0x1033, 0x1034, 0x1035,
    0x1039, 0x103a, 0x103b, 0x103c, 0x103d, 0x103e, 0x103f,
    0x104e, 
    0x1050, 0x1051, 0x1052, 0x1053, 0x1054, 0x1055, 0x1056, 0x1057, 0x1058, 0x1059,
    0x105a, 0x105b, 0x105c, 0x105d, 0x105e, 0x105f,
    0x1098, 0x1099, 0x109a, 0x109b, 0x109c, 0x109d, 0x109e, 0x109f
    ])
    
def printExceptions():
  # Show list of non-standard characters with a standard consonant U+1002.
  result = u'\u1002\u1031 \u1002\u103c'
  for x in nonStd.raw_range:
    result += u'\u1002' + unichr(x) +  ' '
  print result

def main(argv=None):
  printExceptions()


if __name__ == "__main__":
    print 'ARGS = %s' % sys.argv 
    sys.exit(main(sys.argv))