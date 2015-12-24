#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re
import sys

import transliterate
import translit_myazedi
import translit_zawgyi


"""Test data from ThanLWinSoft: http://thanlwinsoft.github.io/www.thanlwinsoft.org/

  DocCharConvert-master/firefox-myanmar-converter/test/ZawGyi.html
  """

class zawgyiText():

  def __init__(self):
    # Title is the first item.
    self.thanlwin_data  = [
      u'က်န္းမာေရး နည္းလမ္း မ်ား',
      u'ကြၽႏ္ုပ္ တို့ ၏ ေပ်ာ္ ႐ႊင္ မႈ၊ သာယာဝေျပာ မႈ ႏွင့္ ေအာင္ျမင္ မႈ တို့ သည္ ကြၽႏ္ုပ္ တို့ ၏ က်န္းမာ ျခင္း အေပၚ တြင္ အမ်ား ႀကီး မွီခို ေန ပါ သည္။ ပညာတတ္ ရန္၊ ႂကြယ္ဝ ခ်မ္းသာ ရန္ ႏွင့္ ႀကိဳးပမ္း လုပ္ေဆာင္ မႈ အားလုံး ေအာင္ျမင္ ေစရန္ အတြက္ က်န္းမာေရး သည္ အထူး ပင္ အေရးႀကီး ပါ သည္။ က်န္းမာေရး မ ျပည့္စုံ လႇၽင္ ကြၽႏ္ုပ္ တို့ ၏ ပညာေရး၊ စီးပြားေရး ႁမွင့္တင္ မႈ လုပ္ငန္း မ်ား လုပ္ ႏိုင္ လိမ့္မည္ မ ဟုတ္ ပါ။ သို့ျဖစ္၍ အစဥ္သျဖင့္ က်န္းမာ ေန ရန္ ကြၽႏ္ုပ္ တို့ ႀကိဳးစား ၾက ရ ပါ မည္။',
      u'က်န္းမာေရး ႏွင့္ ျပည့္စုံ ရန္ အတြက္ ေဆာင္႐ြက္ ရန္ နည္းလမ္း မ်ား ကို သိရွိ လိုက္နာ ရ ပါ မည္။ အစားအေသာက္၊ အအိပ္အေန၊ ေလ့က်င့္ခန္း ႏွင့္ သန့္႐ွင္း မႈ တို့ သည္ က်န္းမာေရး အတြက္ လိုအပ္ခ်က္ မ်ား ျဖစ္ ပါ သည္။ အစားအစာ သည္ အသက္ ႐ွင္ မႈ အတြက္ အထူး လိုအပ္ခ်က္ ျဖစ္ ပါ သည္။ ကြၽႏ္ုပ္ တို့ သည္ အသက္ ႐ွင္ ေနႏိုင္ ရန္ အစာ စား ရ ျခင္း ျဖစ္ ၿပီး စားေသာက္ ရန္ အသက္ ႐ွင္ ေန ျခင္း မ ဟုတ္ ပါ။ က်န္းမာ မႈ အတြက္ သင့္ေတာ္ သည့္ ပ⁠႐ို⁠တိန္း၊ သတၱဳ ဓာတ္ မ်ား ႏွင့္ ဗီတာမင္ မ်ား မ်ား စြာ ပါ ဝင္ သည့္ အစာ မ်ား ကို ရယူ စား သုံး ရန္',
      u'လိုအပ္ ပါ သည္။ ကြၽႏ္ုပ္ တို့ ႏွင့္ ေလႇၽာ္ ကန္ သင့္ျမတ္ မည့္ အိပ္စက္ အနားယူ မႈ မွာ လည္း အေရးႀကီး ပါ သည္။ ကြၽႏ္ုပ္ တို့ ၏ ခႏၶာကိုယ္ မွ ႂကြက္သား မ်ား ႏွင့္ အသား မႇၽင္ မ်ား အား ထိန္းသိမ္း ျပဳျပင္ မႈ အတြက္ အိပ္စက္ ျခင္း ႏွင့္ နား ေန ျခင္း တို့ အညီအမႇၽ လိုအပ္ ပါ သည္။ ထို့ေၾကာင့္ လုံေလာက္ စြာ အိပ္စက္ နား ေန ရ ပါ မည္။',
      u'ကိုယ္ ကာယ ေလ့က်င့္ခန္း မ်ား ႏွင့္ သန့္႐ွင္း မႈ တို့ လည္း အေရးႀကီး လိုအပ္ ပါ သည္။ လမ္းေလႇၽာက္ ျခင္း ႏွင့္ အိမ္ တြင္း ေလ့က်င့္ခန္း မ်ား သည္ အစားအေသာက္ စား လို စိတ္ ႏွင့္ စိတ္ ႐ႊင္လန္း မႈ တို့ ကို တိုးပြား ေစ ပါ သည္။ တစ္ ကိုယ္ ေရ သန့္႐ွင္း ေရး က က်န္းမာ မႈ ကို အေထာက္အကူ ျပဳ ပါ သည္။ ေန့စဥ္ ေရခိ်ဳး ျခင္း၊ အစာ မ စား မီ ႏွင့္ စား ၿပီး တိုင္း လက္ မ်ား ကို စနစ္တက် ေဆးေၾကာ ရ ပါ မည္။',
      u'အထက္ပါ က်န္းမာေရး နည္းလမ္း မ်ား ကို လိုက္နာ ေဆာင္႐ြက္ ပါ က ကြၽႏ္ုပ္ တို့ တစ္သက္ တာ အတြက္ က်န္းမာေရး ႏွင့္ ျပည့္စုံ ေန မည္ မွာ ေသခ်ာ ပါ သည္။ ကြၽႏ္ုပ္ တို့ က်န္းမာ ေန လႇၽင္ စီးပြား ဥစၥာ ျပည့္စုံ ျခင္း၊ ပညာေရး ျပည့္စုံ ျခင္း ႏွင့္ အျခား ေအာင္ျမင္ မႈ မ်ား ကို စြမ္းေဆာင္ ႏိုင္ ပါ မည္။ သို့ပါ၍ က်န္းမာ ျခင္း သည္ ခ်မ္းသာ ျခင္း ျဖစ္ေၾကာင္း ႏွင့္ က်န္းမာ ျခင္း သည္ ခ်မ္းသာ ျခင္း ထက္ ပိုမို ေကာင္းမြန္ သည္ ဟု ဆို ရ မည္ ျဖစ္ ပါ သည္။'
    ]
    self.extraText = u'က်န္းမာေရး နည္းလမ္း မ်ား Some English text in the middle က်န္းမာေရး နည္းလမ္း မ်ား'


# Unicode version of the same text.
# Title is the first item.
class unicodeText():

  def __init__(self):
    self.thanlwin_data  = [
      u'ကျန်းမာရေး နည်းလမ်း များ',
      u'ကျွန်ုပ် တို့ ၏ ပျော် ရွှင် မှု၊ သာယာဝပြော မှု နှင့် အောင်မြင် မှု တို့ သည် ကျွန်ုပ် တို့ ၏ ကျန်းမာ ခြင်း အပေါ် တွင် အများ ကြီး မှီခို နေ ပါ သည်။ ပညာတတ် ရန်၊ ကြွယ်ဝ ချမ်းသာ ရန် နှင့် ကြိုးပမ်း လုပ်ဆောင် မှု အားလုံး အောင်မြင် စေရန် အတွက် ကျန်းမာရေး သည် အထူး ပင် အရေးကြီး ပါ သည်။ ကျန်းမာရေး မ ပြည့်စုံ လျှင် ကျွန်ုပ် တို့ ၏ ပညာရေး၊ စီးပွားရေး မြှင့်တင် မှု လုပ်ငန်း များ လုပ် နိုင် လိမ့်မည် မ ဟုတ် ပါ။ သို့ဖြစ်၍ အစဉ်သဖြင့် ကျန်းမာ နေ ရန် ကျွန်ုပ် တို့ ကြိုးစား ကြ ရ ပါ မည်။',
  
      u'ကျန်းမာရေး နှင့် ပြည့်စုံ ရန် အတွက် ဆောင်ရွက် ရန် နည်းလမ်း များ ကို သိရှိ လိုက်နာ ရ ပါ မည်။ အစားအသောက်၊ အအိပ်အနေ၊ လေ့ကျင့်ခန်း နှင့် သန့်ရှင်း မှု တို့ သည် ကျန်းမာရေး အတွက် လိုအပ်ချက် များ ဖြစ် ပါ သည်။ အစားအစာ သည် အသက် ရှင် မှု အတွက် အထူး လိုအပ်ချက် ဖြစ် ပါ သည်။ ကျွန်ုပ် တို့ သည် အသက် ရှင် နေနိုင် ရန် အစာ စား ရ ခြင်း ဖြစ် ပြီး စားသောက် ရန် အသက် ရှင် နေ ခြင်း မ ဟုတ် ပါ။ ကျန်းမာ မှု အတွက် သင့်တော် သည့် ပ⁠ရို⁠တိန်း၊ သတ္တု ဓာတ် များ နှင့် ဗီတာမင် များ များ စွာ ပါ ဝင် သည့် အစာ များ ကို ရယူ စား သုံး ရန်',

      u'လိုအပ် ပါ သည်။ ကျွန်ုပ် တို့ နှင့် လျှော် ကန် သင့်မြတ် မည့် အိပ်စက် အနားယူ မှု မှာ လည်း အရေးကြီး ပါ သည်။ ကျွန်ုပ် တို့ ၏ ခန္ဓာကိုယ် မှ ကြွက်သား များ နှင့် အသား မျှင် များ အား ထိန်းသိမ်း ပြုပြင် မှု အတွက် အိပ်စက် ခြင်း နှင့် နား နေ ခြင်း တို့ အညီအမျှ လိုအပ် ပါ သည်။ ထို့ကြောင့် လုံလောက် စွာ အိပ်စက် နား နေ ရ ပါ မည်။',

      u'ကိုယ် ကာယ လေ့ကျင့်ခန်း များ နှင့် သန့်ရှင်း မှု တို့ လည်း အရေးကြီး လိုအပ် ပါ သည်။ လမ်းလျှောက် ခြင်း နှင့် အိမ် တွင်း လေ့ကျင့်ခန်း များ သည် အစားအသောက် စား လို စိတ် နှင့် စိတ် ရွှင်လန်း မှု တို့ ကို တိုးပွား စေ ပါ သည်။ တစ် ကိုယ် ရေ သန့်ရှင်း ရေး က ကျန်းမာ မှု ကို အထောက်အကူ ပြု ပါ သည်။ နေ့စဉ် ရေချိုး ခြင်း၊ အစာ မ စား မီ နှင့် စား ပြီး တိုင်း လက် များ ကို စနစ်တကျ ဆေးကြော ရ ပါ မည်။',

      u'အထက်ပါ ကျန်းမာရေး နည်းလမ်း များ ကို လိုက်နာ ဆောင်ရွက် ပါ က ကျွန်ုပ် တို့ တစ်သက် တာ အတွက် ကျန်းမာရေး နှင့် ပြည့်စုံ နေ မည် မှာ သေချာ ပါ သည်။ ကျွန်ုပ် တို့ ကျန်းမာ နေ လျှင် စီးပွား ဥစ္စာ ပြည့်စုံ ခြင်း၊ ပညာရေး ပြည့်စုံ ခြင်း နှင့် အခြား အောင်မြင် မှု များ ကို စွမ်းဆောင် နိုင် ပါ မည်။ သို့ပါ၍ ကျန်းမာ ခြင်း သည် ချမ်းသာ ခြင်း ဖြစ်ကြောင်း နှင့် ကျန်းမာ ခြင်း သည် ချမ်းသာ ခြင်း ထက် ပိုမို ကောင်းမွန် သည် ဟု ဆို ရ မည် ဖြစ် ပါ သည်။'
    ]
    self.extraText = u'ကျန်းမာရေး နည်းလမ်း များ Some English text in the middle ကျန်းမာရေး နည်းလမ်း များ'

# Myazedi version of the same text.
# Title is the first item.
class myazediText():
    # Transformed from Zawgyi to Myazedi via: http://burglish.my-mm.org/latest/trunk/web/fontconv.htm

  def __init__(self):
    self.thanlwin_data  = [
      u'ကဵန္းမာေရး နည္းလမ္း မဵား',
      u'က႗ႎ္ုပ္ တို့ ၏ ေပဵာ္ ႟ၿင္ မႁ၊ သာယာဝေဴပာ မႁ ႎႀင့္ ေအာင္ဴမင္ မႁ တို့ သည္ က႗ႎ္ုပ္ တို့ ၏ ကဵန္းမာ ဴခင္း အေပၞ တၾင္ အမဵား ႒ကီး မႀီခို ေန ပၝ သည္။ ပညာတတ္ ရန္၊ ႑ကၾယ္ဝ ခဵမ္းသာ ရန္ ႎႀင့္ ႒ကိႂးပမ္း လုပ္ေဆာင္ မႁ အားလုံး ေအာင္ဴမင္ ေစရန္ အတၾက္ ကဵန္းမာေရး သည္ အထူး ပင္ အေရး႒ကီး ပၝ သည္။ ကဵန္းမာေရး မ ဴပည့္စုံ လၟဵင္ က႗ႎ္ုပ္ တို့ ၏ ပညာေရး၊ စီးပၾားေရး ႐မႀင့္တင္ မႁ လုပ္ငန္း မဵား လုပ္ ႎိုင္ လိမ့္မည္ မ ဟုတ္ ပၝ။ သို့ဴဖစ္၍ အစဥ္သဴဖင့္ ကဵန္းမာ ေန ရန္ က႗ႎ္ုပ္ တို့ ႒ကိႂးစား ဳက ရ ပၝ မည္။',
      u'ကဵန္းမာေရး ႎႀင့္ ဴပည့္စုံ ရန္ အတၾက္ ေဆာင္႟ၾက္ ရန္ နည္းလမ္း မဵား ကို သိရႀိ လိုက္နာ ရ ပၝ မည္။ အစားအေသာက္၊ အအိပ္အေန၊ ေလ့ကဵင့္ခန္း ႎႀင့္ သန့္႟ႀင္း မႁ တို့ သည္ ကဵန္းမာေရး အတၾက္ လိုအပ္ခဵက္ မဵား ဴဖစ္ ပၝ သည္။ အစားအစာ သည္ အသက္ ႟ႀင္ မႁ အတၾက္ အထူး လိုအပ္ခဵက္ ဴဖစ္ ပၝ သည္။ က႗ႎ္ုပ္ တို့ သည္ အသက္ ႟ႀင္ ေနႎိုင္ ရန္ အစာ စား ရ ဴခင္း ဴဖစ္ ႓ပီး စားေသာက္ ရန္ အသက္ ႟ႀင္ ေန ဴခင္း မ ဟုတ္ ပၝ။ ကဵန္းမာ မႁ အတၾက္ သင့္ေတာ္ သည့္ ပ⁠႟ို⁠တိန္း၊ သတၨႂ ဓာတ္ မဵား ႎႀင့္ ဗီတာမင္ မဵား မဵား စၾာ ပၝ ဝင္ သည့္ အစာ မဵား ကို ရယူ စား သုံး ရန္',
      u'လိုအပ္ ပၝ သည္။ က႗ႎ္ုပ္ တို့ ႎႀင့္ ေလၟဵာ္ ကန္ သင့္ဴမတ္ မည့္ အိပ္စက္ အနားယူ မႁ မႀာ လည္း အေရး႒ကီး ပၝ သည္။ က႗ႎ္ုပ္ တို့ ၏ ခႎၭာကိုယ္ မႀ ႑ကၾက္သား မဵား ႎႀင့္ အသား မၟဵင္ မဵား အား ထိန္းသိမ္း ဴပႂဴပင္ မႁ အတၾက္ အိပ္စက္ ဴခင္း ႎႀင့္ နား ေန ဴခင္း တို့ အညီအမၟဵ လိုအပ္ ပၝ သည္။ ထို့ေဳကာင့္ လုံေလာက္ စၾာ အိပ္စက္ နား ေန ရ ပၝ မည္။',
      u'ကိုယ္ ကာယ ေလ့ကဵင့္ခန္း မဵား ႎႀင့္ သန့္႟ႀင္း မႁ တို့ လည္း အေရး႒ကီး လိုအပ္ ပၝ သည္။ လမ္းေလၟဵာက္ ဴခင္း ႎႀင့္ အိမ္ တၾင္း ေလ့ကဵင့္ခန္း မဵား သည္ အစားအေသာက္ စား လို စိတ္ ႎႀင့္ စိတ္ ႟ၿင္လန္း မႁ တို့ ကို တိုးပၾား ေစ ပၝ သည္။ တစ္ ကိုယ္ ေရ သန့္႟ႀင္း ေရး က ကဵန္းမာ မႁ ကို အေထာက္အကူ ဴပႂ ပၝ သည္။ ေန့စဥ္ ေရခိဵႂး ဴခင္း၊ အစာ မ စား မီ ႎႀင့္ စား ႓ပီး တိုင္း လက္ မဵား ကို စနစ္တကဵ ေဆးေဳကာ ရ ပၝ မည္။',
      u'အထက္ပၝ ကဵန္းမာေရး နည္းလမ္း မဵား ကို လိုက္နာ ေဆာင္႟ၾက္ ပၝ က က႗ႎ္ုပ္ တို့ တစ္သက္ တာ အတၾက္ ကဵန္းမာေရး ႎႀင့္ ဴပည့္စုံ ေန မည္ မႀာ ေသခဵာ ပၝ သည္။ က႗ႎ္ုပ္ တို့ ကဵန္းမာ ေန လၟဵင္ စီးပၾား ဥစၤာ ဴပည့္စုံ ဴခင္း၊ ပညာေရး ဴပည့္စုံ ဴခင္း ႎႀင့္ အဴခား ေအာင္ဴမင္ မႁ မဵား ကို စၾမ္းေဆာင္ ႎိုင္ ပၝ မည္။ သို့ပၝ၍ ကဵန္းမာ ဴခင္း သည္ ခဵမ္းသာ ဴခင္း ဴဖစ္ေဳကာင္း ႎႀင့္ ကဵန္းမာ ဴခင္း သည္ ခဵမ္းသာ ဴခင္း ထက္ ပိုမို ေကာင္းမၾန္ သည္ ဟု ဆို ရ မည္ ဴဖစ္ ပၝ သည္။'
    ]
    self.extraText = u'ကဵန္းမာေရး နည္းလမ္း မဵား Some English text in the middle ကဵန္းမာေရး နည္းလမ္း မဵား'


# Tests to confirm that the conversion continues to work.
class translitRegression():

  def __init__(self):
    # Create transliterators.  
    self.zToU = transliterate.Transliterate(
      translit_zawgyi.ZAWGYI_UNICODE_TRANSLITERATE)
  
    self.mToU = transliterate.Transliterate(
      translit_myazedi.MYAZEDI_UNICODE_TRANSLITERATE)

  def listTest(self):
    # Try list input with short tests.
    zList = [
      u'\u1006\u103a\u108c\u1033\u1044\u1039\u1025\u103a\u1036\u103b\u103c\u1004',
      u'\u1002\u103a\u1064\u1005\u108c\u1006\u108d\u106a\u1025\u102e',
      u'\u1002\u103a\u1064\u1005\u1072']
    resultList = self.zToU.transliterate(zList)
    eList = [u'င်္ဆျီု|၎်ဥျံြွင', u'င်္ဂျင်္စီင်္ဆံဉဦ', u'င်္ဂျစ္တ']

    testResults = []
    for i in xrange(len(resultList)):
      if resultList[i] == eList[i]:
        result = '+ testList %d passes' % i
        print result
      else:
        result = '- testList %d fails' % i
        print result
        print '    Z input =      %s' % transliterate.uStringToHex(zList[i])
        print '    Result hex =   %s' % transliterate.uStringToHex(resultList[i])
        print '    Expected hex = %s' % transliterate.uStringToHex(eList[i])
      testResults.append(result)
    return testResults
        
  def testExtra(self):
    # Check that the extra short lines convert.
    zT = zawgyiText()
    mT = myazediText()
    uT = unicodeText()
    uFromZ = self.zToU.transliterate(zT.extraText)
    testResults = []
    
    if uFromZ != uT.extraText:
      result = 'Extra from Zawgi fails'
    else:
      result = 'Pass! Extra from Zawgi'
    testResults.append(result)
 
    uFromM = self.mToU.transliterate(mT.extraText)
    if uFromM != uT.extraText:
      result = 'Extra from Myazedi fails'
    else:
      result = 'Pass! Extra from Myazedi'
    testResults.append(result)
    return testResults
 
  def testParagraphs(self):
    # Check that the longer paragraphs still convert.
    zT = zawgyiText()
    mT = myazediText()
    uT = unicodeText()
    testResults = []
    for i in xrange(len(zT.thanlwin_data)):
      uFromZ = self.zToU.transliterate(zT.thanlwin_data[i])
      if uFromZ != uT.thanlwin_data[i]:
        result = ['Fail: Z [%d] (%d vs %d) ' % (i,
          len(uT.thanlwin_data[i]), len(uFromZ)),
          uT.thanlwin_data[i], uFromZ]
      else:
        result = 'Z [%d] pass!' % i
      testResults.append(result)
      
    # Check that the extras still convert.
    for i in xrange(len(mT.thanlwin_data)):
      uFromM = self.mToU.transliterate(mT.thanlwin_data[i])
      if uFromM != uT.thanlwin_data[i]:
        result = ['Fail: M [%d] (%d vs %d) ' % (i,
          len(uT.thanlwin_data[i]), len(uFromM)),
          uT.thanlwin_data[i], uFromM]
      else:
        result = 'M [%d] pass!' % i
      testResults.append(result)
    return testResults

  def testZeroWidthSpace(self):
    inTextWith200b = u'စမ္​းၾကည္​့လိုက္​ဦမယ္​'
    inTextWithout200b = u'စမ္းၾကည့္လိုက္ဦမယ္'
    zExpected = u'စမ်းကြည့်လိုက်ဦမယ်'
    mExpected = u'စမ်ွးကည့်လိုက်ဦမယ်'
    uFromZ = self.zToU.transliterate(inTextWith200b)
    uFromM = self.mToU.transliterate(inTextWith200b)

    testResults = []
    if uFromZ == zExpected and uFromM == mExpected:
      result = "Strings with 200b pass!"
    else:
       result = "Strings with 200b fail."
    testResults.append(result)

    uFromZ = self.zToU.transliterate(inTextWithout200b)
    uFromM = self.mToU.transliterate(inTextWithout200b)
    if uFromZ == zExpected and uFromM == mExpected:
      result = "Strings without 200b pass!"
    else:
       result = "Strings without 200b fail."
    testResults.append(result) 
    
    return testResults    
    
  def runAllTests(self):
    print self.testExtra()
    for r in self.testParagraphs():
      print r
    print self.listTest()
    print self.testZeroWidthSpace()


# Run all the tests.
def main(argv=None):

  test = translitRegression()
  test.runAllTests()
  

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
