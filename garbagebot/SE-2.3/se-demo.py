# -*- coding: utf_8 -*-

# execfile (dist/SE-demo.py)


import SE



# Iterates through most of the examples in 'se-doc.htm' prompting for what next:
#
# Number (e.g. 3.7.1.), S(how compile), N(ext) or Q(uit)? > 
#
# Number refer to the doc.




def run_demo ():

   i =  0   # index of group
   j = -1   # index of example in group
   l =  1   # number of examples of group
   E = None

   while 1:
      response = raw_input ('Number (e.g. 3.7.1.), S(how compile), N(ext) or Q(uit)? > ')
      if response:
         r = response [0]
         if r in 'Ss':
            if E:
               print '\n'
               for T in E.Translators:
                  T.show ()
               print '\n'
               E.show_log (1)
               print
         elif r in 'Qq':
            print
            return
         elif r in 'Nn':
            j += 1
            if j == l:
               i = (i + 1) % len (tests_ordered)
               j = 0
               l = len (tests [tests_ordered [i]])
            group = tests [tests_ordered [i]]
            print
            pass_or_fail, E = group [j] ()
         else:
            if response [-1] != '.':
               response += '.'
            if response not in tests_ordered:
               print 'No such example %s' % response
               continue 
            i = tests_ordered.index (response)
            j = 0
            group = tests [tests_ordered [i]]
            l = len (group)
            print
            pass_or_fail, E = group [j] ()
         response = ''
         print


def test (definitions, data, solution, E = None):
   print '\nDefinitions: \'%s\'' % definitions
   print 'Data:        \'%s\'' % data
   if E == None:
      exec ('E = SE.SE (definitions)')
      exec ("s = E (data)")
   else:
      s = E (data)
   print 'SE makes:    \'%s\'' % s
   print '\nExpected:    \'%s\'' % solution
   if s == solution:
      print '\nOkay\n'
      pass_or_fail = 0
   else:
      for i in range (min (len (s), len (solution))):
         if s[i] != solution[i]:
            break
      print '\nNot okay from position %d\n' % i
      if i < 40: ii = 0
      else: ii = i - 40
      s_display = s [ii:ii+80]
      solution_display = solution [ii:ii+80]
      print 'Made    : ' + repr (s_display)
      print 'Expected: ' + repr (solution_display)
      stretch = 0
      for iii in range (ii, i):
         c = s_display [iii]
         if c in '\t\r\n\f\v\a':
            stretch += 1
         elif ord (c) < 32 or ord (c) > 127:
            stretch += 3
      print (10 + i-ii+stretch) * ' ' + '/\\'
      print
      response = raw_input ('\nShow compile and log? (S or Y) > ')
      if response and response [0] in 'SsYy':
         print '\n'
         E.Translators[0].show ()
         print '\n'
         E.show_log (1)
         print
      pass_or_fail = -1

   return pass_or_fail, E


def _221 ():
   print '\n2.2.1. - Definition format \'old=new\'.'
   definitions = 'old=new'
   data = "If 'old' reads 'new' we know it works."
   solution = "If 'new' reads 'new' we know it works."
   pass_or_fail, E = pass_or_fail, E = test (definitions, data, solution)
   return pass_or_fail, E


def _222 ():
   print '\n2.2.2. - A definition with a missing substitute is a deletion.'
   definitions = 'HORROR='
   data = 'This >HORROR< must be deleted!'
   solution = 'This >< must be deleted!'
   pass_or_fail, E = pass_or_fail, E = test (definitions, data, solution)
   return pass_or_fail, E


def _223 ():
   print '\n2.2.3. - A target can be a regular expression'
   definitions = '~123-45678-[0-3][012ABF]?~=***'
   data = 'Client: 123-45678, Account Numbers: 123-45678-00, 123-45678-01 and 123-45678-0B'
   solution = 'Client: 123-45678, Account Numbers: ***, *** and ***'
   pass_or_fail, E = test (definitions, data, solution)
   return pass_or_fail, E


def _224 ():
   print '\n2.2.4. - A substitute in angled brackets is a file name'
   print '\nFile_Catenator = SE.SE (\'F1=<file.1> F2=<file.2> F3=<file.3>\')'
   print '\nMake component files and try.\n'
   return 0, None


def _23 ():
   print '\n2.3. - A definition set can have an arbitrary number of definitions.'
   definitions = 'cop=officer joker=person chickenshit=triviality guy=gentleman yell=smile'
   data = 'The guy yelled at the cop: What kind of a joker are you anyway to bother with such chickenshit?'
   solution = 'The gentleman smiled at the officer: What kind of a person are you anyway to bother with such triviality?'
   pass_or_fail, E = test (definitions, data, solution)
   return pass_or_fail, E


def _242_a_wrong ():
   print '\n2.4.2. - Error: Double quotes must brace entire definition, not just one side.'
   definitions = ' "          =ten spaces" "spread=s p r e a d" "u n s p r e a d"=unspread '
   data = '             spread u n s p r e a d'
   solution = 'ten spaces   s p r e a d unspread'
   pass_or_fail, E = test (definitions, data, solution)
   return pass_or_fail, E


def _242_a_right ():
   print '\n2.4.2. - Correct: Double quotes must brace entire definition, not just one side.'
   definitions = ' "          =ten spaces" "spread=s p r e a d" "u n s p r e a d=unspread" '
   data = '             spread u n s p r e a d'
   solution = 'ten spaces   s p r e a d unspread'
   pass_or_fail, E = test (definitions, data, solution)
   return pass_or_fail, E


def _242_b ():
   print '\n2.4.2. - Double-quoted definitions span multiple lines'
   definitions = '''
"TB=Mr. Tony Blair
Downing Street 10
London
"
"GB=Mr. George Bush
The White House
Washington DC
" '''
   data = '\nGB\nTB'
   solution ='''
Mr. George Bush
The White House
Washington DC

Mr. Tony Blair
Downing Street 10
London
'''
   pass_or_fail, E = test (definitions, data, solution)
   return pass_or_fail, E


def _242_c_wrong ():
   print '\n2.4.2. - Error: failure to quote back-slashed white space.'
   definitions = 'word\tanother_word\nnew_line=whatever'
   data = 'word\tanother_word\nnew_line'
   solution = 'whatever'
   pass_or_fail, E = test (definitions, data, solution)
   return pass_or_fail, E


def _242_c_right ():
   print '\n2.4.2. - Correct: back-slashed white space characters quoted'
   definitions = '"word\tanother_word\nnew_line=whatever"'
   data = 'word\tanother_word\nnew_line'
   solution = 'whatever'
   pass_or_fail, E = test (definitions, data, solution)
   return pass_or_fail, E


def _242_d ():
   print '\n2.4.2. - C-code block-comment eater'
   definitions = ' "~[\n\s]*/\*(.|\n)*?\*/~=" '
   data ='''
int do_something_n_times (int n):
{
   /* Change function name: does ten times, not n times
    */
   int i = 10;
   /* 7/13/2006 11:01AM
    * do_something fixed: returned sum
    */
   while i:
     i--;
     n += do_something (i);
   ... etc.
}'''
   solution ='''
int do_something_n_times (int n):
{
   int i = 10;
   while i:
     i--;
     n += do_something (i);
   ... etc.
}'''
   pass_or_fail, E = test (definitions, data, solution)
   return pass_or_fail, E


def _243 ():
   print '\n2.4.3. - The target place holder \'=\' combines with other data.'
   definitions = '"New York==: (-73.96, 40.76)" "Tokyo==: (139.77, 35.68)"'
   data = 'New York, Tokyo'
   solution = 'New York: (-73.96, 40.76), Tokyo: (139.77, 35.68)'
   pass_or_fail, E = test (definitions, data, solution)
   return pass_or_fail, E


def _243_a ():
   print '\n2.4.3. - Overlapping targets.'
   definitions = 'be=BE being=BEING been=BEEN bee=BEE belong=BELONG long=LONG longer=LONGER'
   data = "There was a bee belonging to hive nine longing to be a beetle and thinking that being a bee was okay, but she had been a bee long enough and wouldn't be one much longer."
   solution = "There was a BEE BELONGing to hive nine LONGing to BE a BEEtle and thinking that BEING a BEE was okay, but she had BEEN a BEE LONG enough and wouldn't BE one much LONGER."
   pass_or_fail, E = test (definitions, data, solution)
   return pass_or_fail, E

 
def _243_ba ():
   print '\n2.4.3. - Precedence with regular expressions.'
   definitions = '~[aeiou]+~=vowels  "~a+~=string of a"'
   data = 'aaaaa'
   solution = 'string of a'
   pass_or_fail, E = test (definitions, data, solution)
   return pass_or_fail, E


def _243_bb ():
   print '\n2.4.3. - Precedence with regular expressions.'
   definitions = '"~a+~=string of a" ~[aeiou]+~=vowels'
   data = 'aaaaa'
   solution = 'vowels'
   pass_or_fail, E = test (definitions, data, solution)
   return pass_or_fail, E


def _243_bc ():
   print '\n2.4.3. - Precedence with regular expressions.'
   definitions = ' aaaaa=5a  "~a+~=string of a" ~[aeiou]+~=vowels'
   data = 'aaaaa'
   solution = '5a'
   pass_or_fail, E = test (definitions, data, solution)
   return pass_or_fail, E


def _243_ca ():
   print '\n2.4.3. - Precedence with regular expressions.'
   definitions = '<EAT> "~[aeiou][aeiou]~== "'
   data = 'Look and see all double vowels including repeating pairs'
   solution = 'oo ee ou ea ai '
   pass_or_fail, E = test (definitions, data, solution)
   return pass_or_fail, E


def _243_cb ():
   print '\n2.4.3. - Precedence with regular expressions.'
   definitions = '<EAT> aa= ee= ii= oo= uu= "~[aeiou][aeiou]~== "'
   data = 'Look and see all double vowels but no repeating pairs'
   solution = 'ou ea ai '
   pass_or_fail, E = test (definitions, data, solution)
   return pass_or_fail, E


def _244 ():

 # definitions                target          substitute

   definitions = (
   ( '/ =space',                 ' ',           'space'),
   ( '#=comment',                '#',           'comment'),
   ( '\#=comment',               '#',           'comment'),
   ( '(35)=comment',             '#',           'comment'),
   ( '~=tilde',                  '~',           'tilde'),
   ( '(126)=tilde',              '~',           'tilde'),
   ( '~~=2-tilde',                '~~',          '2-tilde'),
   ( '(126)(126)=2-tilde',       '~~',          '2-tilde'),
   ( '\~~=2-tilde',              '~~',          '2-tilde'),
   ( '\~[a-z]~=not(32)regex',    '~[a-z]~',     'not regex'),
   ( '(126)[a-z]~=not(32)regex', '~[a-z]~',     'not regex'),
   ( '"=double quote"',          '"',           'double quote"'),
   (r'\"=double quote"',        r'\"',          'double quote"'),
   ( '""=double quote"',         '"',           'double quote'),
   ( '\""=2-double-quotes"',     '""',          '2-double-quotes"'),
   ( '(34)=double-quote"',       '"',           'double-quote"'),
   ( '"(34)=double quote"',      '"',           'double quote'),
   (r'\=backslash',              '\\',          'backslash'),
   (r'\\=backslash',             '\\\\',        'backslash'),
   ( '(92)=backslash',           '\\',          'backslash'),
   ( '\=\==\=\=:(32)equality',   '==',          '==: equality'),
   ( '\=\===:(32)equality',      '==',          '==: equality'),
   ( '(x3d)(x3d)==:(32)equality','==',          '==: equality'),
   ( '\(88)=X',                  '(88)',        'X'),
   ( '(88\)=X',                 r'(88\)',       'X'),
   (r'\\(88)=X',                r'\(88)',       'X'),
   ( ':B:=<b>',                  ':B:',         '(file data)'),
   ( ':B:=\<b>',                 ':B:',         '<b>'),
   ( ':B:=<b\>',                 ':B:',         '<b\>'),
   ( '(257)\#~"~=unambiguous',   '(257)\#~"~',  'unambiguous'),
   ( 'assignment==',             'assignment',  'assignment'),
   ( 'assignment=(x3d)',         'assignment',  '='),
   ( 'assignment=\=',            'assignment',  '='),
   (r'C:\temp\=TEMPDIR',         'C:\\temp\\',  'TEMPDIR'),
   (r'C:\temp(92)=TEMPDIR',      'C:\\temp\\',  'TEMPDIR'),
  )
  
   pass_or_fail = 0
   E = None
   quit = 0
   for definition, target, substitute in definitions:
      print '\n2.4.4. - A bunch of tricky definitions.\n'
      pass_or_fail, E = test (definition, target, substitute)
      while 1:
         response = raw_input ('S(how compile), N(ext), Q(uit Tricky Definitions) > ')
         try: r = response [0]
         except IndexError: r = ''
         if r and r.upper () in 'SNQ':
            break
      print
      if r in 'Ss':
         print '\n'
         for T in E.Translators:
            T.show ()
         print '\n'
         E.show_log (1)
         print
      if r in 'Qq':
         break

   return pass_or_fail, E


def _32 ():
   import time
   print '\n3.2. - Definition files.\n'
   definitions = '''
   Sun=dimanche, Mon=lundi, Tue=mardi, Wed=mercredi,
   Thu=jeudi, Fri=vendredi, Sat=samedi,
   Jan=janvier  Feb=f‚vrier Mar=mars   Apr=avril  May=mai  Jun=juin
   Jul=juillet  Aug=ao–t  Sep=septembre Oct=octobre Nov=novembre Dec=d‚cembre'''
   print '\nDefinitions: \'%s\'' % definitions
   print 'Data:        time.ctime ()'
   E = SE.SE (definitions)
   print 'SE makes:    \'%s\'' % E (time.ctime ())
   print '\n'
   file_name = raw_input ('Name a new file to save French Ctime (Hit return to skip this test) > ')
   print
   if file_name:
      E.save (file_name)
      print 'Running from file'
      print SEL.SEL (file_name) (time.ctime ())
      print '\n'
   response = raw_input ('Show compile? (S or Y) > ')
   try: r = response [0]
   except IndexError: r = ''
   if r in 'SsYy':
      print '\n'
      for T in E.Translators:
         T.show ()
      print
   return 0, E


def _33_a ():
   print '\n3.3. - Merging substitution sets.\n'
   print "Ids_To_Symbol = SE.SE ('cusip2symbol.se isin2symbol.se sec2symbol.se')\n"
   print 'The first example merges three definition files.'
   print 'You\'ll have to make your own to see it work.\n'
   return 0, None


def _33_b ():
   print '\n2.4.3. - Merging substitution sets.\n'
   print "\nThe first two definitions fill in for a file 'common_abbreviations.se'\n"
   definitions = ' "United States=U.S." "Department of Transportation=DoT" Trinitrotoluene=TNT "Chemicals Register=CR"'
   data = "Trinitrotoluene was added to the 'Chemicals Register Part 19-A' of the United States Department of Transportation."
   solution = "TNT was added to the 'CR Part 19-A' of the U.S. DoT."
   pass_or_fail, E = test (definitions, data, solution)
   return pass_or_fail, E


def _34 ():
   print '\n3.4. - Redefinition.\n'
   definitions = 'old=antique old=aged'
   data = 'old people'
   solution = 'aged people'
   pass_or_fail, E = test (definitions, data, solution)
   return pass_or_fail, E


def _341 ():
   print '\n3.4.1. - Exception.\n'
   print "\nThe first definition fills in for a file 'unabbreviations.se'\n"
   definitions = ' "B.A.=Bachelor of Arts" "B.A. fellow=British Academy fellow"'
   data = '... October 1958: B.A. ... March 1976: B.A. fellowship ...'
   solution = '... October 1958: Bachelor of Arts ... March 1976: British Academy fellowship ...'
   pass_or_fail, E = test (definitions, data, solution)
   return pass_or_fail, E

   
def _342_a ():
   print '\n3.4.2. - Target lock.\n'
   definitions = '(13)(10)=(32) (10)=(32) (13)(10)(13)(10)== (10)(10)== "~\r?\n[ \t]~=="'
   data = 'One\nword\nper\nline.\n\nNew\nparagraph.\n   Indented\nparagraph'
   solution = 'One word per line.\n\nNew paragraph.\n   Indented paragraph'
   pass_or_fail, E = test (definitions, data, solution)
   return pass_or_fail, E


def _342_b ():
   print '\n3.4.2. - Target lock.\n'
   print "SE.SE ('foundation/anonymize_member_names.se \"Barbara Kycenuk==\"') ('foundation/board/Feb-19', '')"
   print '\nTest involves a definition file. Make your own to test.\n'
   return 0, None


def _351 ():
   print '\n3.5.1. - Deletion filter.\n'
   whacking_the_dragon = ' "terrifying dragon=" '
   definitions = whacking_the_dragon
   data = 'woods, rivers, castle, king, princess, mountains, terrifying dragon, people, towns, lakes '
   solution = 'woods, rivers, castle, king, princess, mountains, , people, towns, lakes '
   pass_or_fail, E = test (definitions, data, solution)
   return pass_or_fail, E


def _352 ():
   print '\n3.5.2. - Extraction filter.\n'
   whacking_the_dragon = ' "terrifying dragon=dead dragon" '
   everyone_stay_home = ' '.join (['(x%x)=' % n for n in range (256)])
   except_the_princess = ' princess=princess (32)== '
   definitions = whacking_the_dragon + everyone_stay_home + except_the_princess
   data = "I don't give a damn what kind of kingdom this is and what's in it as long as there's a terrifying dragon and a princess."
   solution = '                    dead dragon   princess'
   pass_or_fail, E = test (definitions, data, solution)
   return pass_or_fail, E


def _353_a ():
   print '\n3.5.3. - Null edit modes.\n'
   definitions = ''
   data = 'We expect the input stream to come out unaltered.'
   solution = 'We expect the input stream to come out unaltered.'
   pass_or_fail, E = test (definitions, data, solution)
   return pass_or_fail, E


def _353_b ():
   print '\n3.5.3. - Null edit modes.\n'
   definitions = '<EAT>'
   data = 'The keyword <EAT> without definitions zaps everything.'
   solution = ''
   pass_or_fail, E = test (definitions, data, solution)
   return pass_or_fail, E


def _361_a ():
   print '\n3.6.1. - Multiple-pass runs.'
   whacking_the_dragon = ' "terrifying dragon=dead dragon" '
   except_the_princess = ' princess=princess (32)== '
   deflate = ' "~ +~= " '
   definitions = whacking_the_dragon + except_the_princess + ' <EAT> | ' + deflate
   data = "I don't give a damn what kind of kingdom this is and what's in it as long as there's a terrifying dragon and a princess."
   solution = ' dead dragon princess'
   pass_or_fail, E = test (definitions, data, solution)
   return pass_or_fail, E
   

def _361_b ():
   print '\n3.6.1. - Multiple-pass runs.'
   definitions = 'A=B | B=C | C=D | D=E | E=F'
   data = 'ABCDEF'
   solution = 'FFFFFF'
   pass_or_fail, E = test (definitions, data, solution)
   return pass_or_fail, E
 

def _362 ():
   print '\n3.6.2. - Nesting calls.'
   print '\nDoesn\'t fit the testing loop format. Make your own test.\n'
   return 0, None


def _371 ():
   print '\n3.7.1. - Setting marks.'
   definitions = '<EAT> "terrifying dragon=+MARK+dead dragon+MARK+" princess=+MARK+=+MARK+ | +MARK+= +MARK++MARK+=,(32)'
   data = "I don't give a damn what kind of kingdom this is and what's in it as long as there's a terrifying dragon and a princess."
   solution = 'dead dragon, princess'
   pass_or_fail, E = test (definitions, data, solution)
   return pass_or_fail, E


def _372 ():
   print '\n3.7.2. - Split marks.'
   definitions = 'lbs=| GBP=| \==| *=| "~[0-9]+\s*x\s*[0-9]+~=|'
   data = 'Crank 2 x 1 6000-2RS1 10 26 8 460 lbs 0.019 * 2 = 0.038 GBP 124.60 (1)'
   solution = 'Crank | 6000-2RS1 10 26 8 460 | 0.019 | 2 | 0.038 | 124.60 (1)'
   pass_or_fail, E = test (definitions, data, solution)
   print '... the rest is basic Python\n'
   return pass_or_fail, E


def _38 ():
   print '\n3.8. - Dynamic targeting.'
   print '\nTest yourself copying from the doc to the IDLE window.\nIt is worth your while.\n'
   return 0, None

 
def _4 ():
   print '\n4. - Working with objects.'
   print '\nMake an Editor and try changing and displaying its settings.\n\n'
   return 0, None


def _415 ():
   print '\n4.1.5. - Intermediate data.'
   definitions = 'A=B | B=C | C=D | D=E | E=F'
   data = 'ABCDEF'
   solution = 'FFFFFF'
   E = SE.SE (definitions)
   E.set (keep_chain = 1)
   print '\nThis tester sets keep_chain for you before running the data: E.set (keep_chain = 1)'
   pass_or_fail, E = test (definitions, data, solution, E)
   print '\nE.show () will now display the intermediate data:'
   E.show ()
   print
   return 0, None


def _417 ():
   print '\n4.1.7. - Saving an editor\'s definitions.'
   print '''\nE.save ( (file name) ) will write the editor's definitions to an editable and compilable 
text file. Try it out. Going back and forth from Editor objects to definitions files makes for an 
extremely flexible and transparent system.\n
''' 
   return 0, None

def _42 ():
   print '\n4.2. - The translator object.'
   print '''
An Editor contains a list of Translators, each of which processes its substitution set
and passes the result on the the next Translator. E.show (show_translators = 1) will call its Translators\' 
method \'show ()\' too.
      Translators can be shown, edited, saved and called to make an inverted copy of themslves (substitute=target).
They can be stuck onto and taken away from Editor objects using standard Python list manipulations. 
Experimenting interactively is very easy.\n
'''
   return 0, None

def _5 ():
   print '\n5. - Input and output.'
   print '''
The HTM manual explains IO in great detail. The IO system is very logical and intuitive.\n
'''
   return 0, None

def _6 ():
   print '\n6. - The message log.'
   print '''
Each editor and Translator object has a message log where non-fatal problems are recorded,
such as dysfunctional definitions or write-protected destination files. E.show_log (show_translators = 1)
will display whatever snags the objects have experienced in their life time. 
      You will have seen logs by now, because this demo displays the log by request if an example 
demonstrates a flop.\n
'''
   return 0, None

def _8 ():
   print '\n8. - Examples.'
   print '''
The examples have all been tested. They merit more attention than this testing routine can solicit. To 
see them work, copy statements from the manual to the IDLE prompt and follow their action step by step.\n
'''
   return 0, None



tests = {
'2.2.1.' : (_221,),
'2.2.1.' : (_221,),
'2.2.2.' : (_222,),
'2.2.2.' : (_222,),
'2.2.3.' : (_223,),
'2.2.3.' : (_223,),
'2.2.4.' : (_224,),
'2.2.4.' : (_224,),
'2.3.'   : (_23,),
'2.4.2.' : (_242_a_wrong,_242_a_right,_242_b,_242_c_wrong,_242_c_right,_242_d,),
'2.4.3.' : (_243,),
'2.4.3.' : (_243,),
'2.4.3.' : (_243_a,_243_ba,_243_bb,_243_bc,_243_ca,_243_cb,),
'2.4.4.' : (_244,),
'2.4.4.' : (_244,),
'3.2.'   : (_32,),
'3.3.'   : (_33_a,_33_b,),
'3.4.'   : (_34,),
'3.4.1.' : (_341,),
'3.4.2.' : (_342_a,_342_b,),
'3.5.1.' : (_351,),
'3.5.2.' : (_352,),
'3.5.3.' : (_353_a,_353_b,),
'3.6.1.' : (_361_a,_361_b,),
'3.6.2.' : (_362,),
'3.7.1.' : (_371,),
'3.7.2.' : (_372,),
'3.8.'   : (_38,),
'4.'     : (_4,),
'4.1.5.' : (_415,),             
'4.1.7.' : (_417,),             
'4.2.'   : (_42,),             
'5.'     : (_5,),
'6.'     : (_6,),
'8.'     : (_8,),
}            
             
tests_ordered = tests.keys ()   
tests_ordered.sort ()


