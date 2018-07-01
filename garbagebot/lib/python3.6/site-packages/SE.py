# SE.PY

# Version 2.3 


import SEL

import sys


__version__   = SEL.__version__
__author__    = SEL.__author__
__copyright__ = SEL.__copyright__



###################################

YES = 1
NO  = 0

_yes_no = 'no', 'yes'


###################################




# Display


_CASCADE_DATA_CLIP = 128  # Prevents the cascade data display from overflowing the screen

_file_protections = (
  'Names of existing file may not be changed',
  'If file exists, translation will be appended',
  'If file exists, translation will take its name',
  'Translation will take the name of the source file',
)



##################################


# Module settings

# SEL.DEFINITION_PATH   (Default is None)

def set (reset = NO, definition_path = None):

   SEL.set (reset, definition_path)


def show ():

   print '\nModule SE - Version 2.3 \n'
   print '  DEFINITION PATH  > %s  (module attribute)\n' % SEL.DEFINITION_PATH
   print 'Special characters\n'
   print '  Quote            > %s' % SEL._SC_QUOTE
   print '  Comment          > %s' % SEL._SC_COMMENT
   print '  Separator        > %s' % SEL._SC_SEPARATOR
   print '  Target           > %s' % SEL._SC_TARGET
   print '  Ascii            > %s' % SEL._SC_ASCII
   print '  Literalizer      > %s' % SEL._SC_LITERALIZER
   print '  Run              > %s' % SEL._SC_RUN
   print '  Regex            > %s' % SEL._SC_REGEX
   print '  File name        > %s\n' % SEL._SC_FILE_NAME



def about ():


   print """

   SE - A Python Stream Editor

   Version 2.3 

   by Frederic Rentsch
   (c) 2006

   SE and SEL are freeware in exchange for authorship credit.

   -----------------------------------------------------------

   More on the Editor and Translator Class:
      SE.SE.__doc__
      SE.SE.__call__.__doc__
      SE.Translator.__doc__

   Read all about it in SE-DOC.HTM


   """



def version ():  return 'SE 2.3  - ' + SEL.version ()




##################################



class SE (SEL.SEL):


   """
      SE - A Python Stream Editor

      Version 2.3 

      by Frederic Rentsch
      (c) 2006

      SE and SEL are freeware in exchange for authorship credit.

      -------------------------------------------------------------------------------------

      SE is a stream editor class whose constructor compiles substitution definitions
      in string form and executes them on any input data.
         SE has a number of methods for interactive development work. If these are not
      required, the functional component of SE, SEL (SE Light), can be used standing alone.

      SE_Object = SE.SE (substitution definitions)

      data_translation = SE_Object (data)

      substitution definitions:

         A string of definitions and / or file names

      Methods:

         __call__ ()                    Takes an input stream and returns a translated output stream
         show (show_translators = 0)    Displays its settings and optionally its Translators
         set (keyword arguments)        For changing runtime settings
         save (file_name)               Writes its definitions to an editable, compilable text file
         SE ()                          Returns a 'light' version of itself (without interactive facilities)

   """

   KEEP_CASCADE       = NO
   CASCADE_DATA_CLIP  = None
   cascade            = None
   Translators        = None


   def __init__ (self, substitutions, file_handling_flag = 0):

      """
         SE.SE ()

         Version 2.3 

         by Frederic Rentsch
         (c) 2006

         SE and SEL are freeware in exchange for authorship credit.

         -----------------------------------------------------------------------------------------------

         SE is a Stream Editor class that compiles serach-and-replace definitions and executes them on
         any input data.

         SE.__doc__ tells more. SE-DOC.HTM tells everything

      """

      if isinstance (substitutions, SEL.SEL):
         Sel = substitutions
         self.Translators = []
         for TL in Sel.Translators:
            self.Translators.append (Translator (TL))
         self.MAX_TARGET_LENGTH  = Sel.MAX_TARGET_LENGTH
         self.INPUT_PATH         = Sel.INPUT_PATH
         self.OUTPUT_PATH        = Sel.OUTPUT_PATH
         self.FILE_HANDLING_FLAG = Sel.FILE_HANDLING_FLAG
         self.BACKUP_EXTENSION   = Sel.BACKUP_EXTENSION
         self.Translator_Class   = Sel.Translator_Class

      else:
         SEL.SEL.__init__ (self, substitutions, file_handling_flag, Translator)

      self.cascade = []
      self.CASCADE_DATA_CLIP = _CASCADE_DATA_CLIP



   def SEL (self):

      S = SE ('')
      S.Translators = []
      for T in self.Translators:
          TL = SEL.Translator ()
          TL.single_byte       = T.single_byte
          TL.single_byte_on    = T.single_byte_on
          TL.multi_byte        = T.multi_byte
          TL.multi_byte_on     = T.multi_byte_on
          TL.hard_regex        = T.hard_regex
          TL.hard_regex_on     = T.hard_regex_on
          TL.soft_regex        = T.soft_regex
          TL.soft_regex_on     = T.soft_regex_on
          TL.NULL_MODE         = T.NULL_MODE
          S.Translators.append (TL)
          S.MAX_TARGET_LENGTH  = self.MAX_TARGET_LENGTH
          S.INPUT_PATH         = self.INPUT_PATH
          S.OUTPUT_PATH        = self.OUTPUT_PATH
          S.FILE_HANDLING_FLAG = self.FILE_HANDLING_FLAG
          S.BACKUP_EXTENSION   = self.BACKUP_EXTENSION
          S.Translator_Class   = self.Translator_Class

      return S



   def show (self, show_translators = NO):

      print '\nSE.DEFINITION_PATH   > %s (Module setting)' % SEL.DEFINITION_PATH
      print '\n', self
      print '\nCompiling'
      print '  MAX_TARGET_LENGTH  > %d'         % self.MAX_TARGET_LENGTH
      print '\nProcessing'
      print '  INPUT_PATH         > %s'         % self.INPUT_PATH
      print '  OUTPUT_PATH        > %s'         % self.OUTPUT_PATH
      print '  FILE_HANDLING_FLAG > %d    (%s)' % (self.FILE_HANDLING_FLAG, _file_protections [self.FILE_HANDLING_FLAG])
      print '  BACKUP_EXTENSION   > %s (Replaced files take this extension)' % (self.BACKUP_EXTENSION)
      print '\nDeveloping'
      print '  KEEP_CASCADE       > %d (%s)'    % (self.KEEP_CASCADE, _yes_no [self.KEEP_CASCADE != 0])
      print '  CASCADE_DATA_CLIP  > %d\n'       % self.CASCADE_DATA_CLIP

      if show_translators:
         for T in self.Translators:
            T.show ()

      if self.KEEP_CASCADE:
         l = len (self.cascade)
         if l > 0:
            print 'Translation Cascade'
            print '-' * 82
            cascade_count = 0
            if type (self.cascade [0]) == str:
               for s in self.cascade:
                  print ' ', s [:self.CASCADE_DATA_CLIP]
                  if cascade_count < l - 1:
                     print cascade_count, '-' * 80
                  cascade_count += 1
            else:
               for f in self.cascade:
                  tell = f.tell ()
                  f.seek (0)
                  s = f.read (self.CASCADE_DATA_CLIP)
                  print ' ', f.name, s
                  if cascade_count < l - 1:
                     print cascade_count, '-' * 80
                  cascade_count += 1
                  f.seek (tell)
            print '-' * 82
      print



   def set (self, reset = NO,
            input_path         = None,
            output_path        = None,
            file_handling_flag = None,
            max_target_length  = None,
            cascade_data_clip  = None,
            backup_extension   = None,
            keep_cascade       = None):

      SEL.SEL.set (self, reset,
            input_path,
            output_path,
            file_handling_flag,
            max_target_length,
            backup_extension)

      if cascade_data_clip != None:
         self.CASCADE_DATA_CLIP = cascade_data_clip
      elif reset:
         self.CASCADE_DATA_CLIP = _CASCADE_DATA_CLIP

      if keep_cascade != None:
         self.KEEP_CASCADE = keep_cascade
      elif reset:
         self.KEEP_CASCADE = NO



   def __call__ (self, input, output = None, cascade_break = None):


      """
         SE - A Python Stream Editor

         Version 2.3 

         by Frederic Rentsch
         (c) 2006

         SE and SEL are freeware in exchange for authorship credit.

         -------------------------------------------------------------------

         SEL.SEL.__call__ (input = None, output = None, cascade_break = None)

         input:

            'abc'        string
            'abc'        input file, if abc is an existing file's name
            ' abc'       string if abc is an existing file's name
            file object  file object open for reading

         output:

            None         same type as input, file name auto-generated
            ''           string
            str          output file name
            file         a file object open for writing

         cascade break:

            For breaking a multi-pass editor prematurely. Says how many
            passes should be done.

         Returns output

         Find an exhaustive discussion on IO typing and multi-pass cascades
         in SE-DOC.HTM

      """

      return SEL.SEL.__call__ (self, input, output, cascade_break)




   def _do_file (self, in_file, out_file_path, cascade_break = None):


      if self.KEEP_CASCADE:
         tell = in_file.tell ()
         in_file.seek (0)
         s = in_file.read (self.CASCADE_DATA_CLIP)
         self.cascade = ['%s: -> %s' % (in_file.name, s)]
         in_file.seek (tell)

      new_file = self.Translators [0].do_file (in_file, out_file_path, self.MAX_TARGET_LENGTH)

      for T in self.Translators [1:]:
         if cascade_break and self.Translators.index (T) >= cascade_break:
            break
         new_file.seek (0)
         newest_file = T.do_file (new_file, out_file_path, self.MAX_TARGET_LENGTH)
         if self.KEEP_CASCADE:
            new_file.seek (0)
            s = new_file.read (self.CASCADE_DATA_CLIP)
            self.cascade.append ('%s: -> %s' % (new_file.name, s))
            new_file.close ()
         else:
            new_file.close ()
            SEL.os.remove (new_file.name)
         new_file = newest_file

      if self.KEEP_CASCADE:
         tell = new_file.tell ()
         new_file.seek (0)
         s = new_file.read (self.CASCADE_DATA_CLIP)
         name = self._out_file_name or new_file.name
         self.cascade.append ('%s: -> %s' % (name, s))
         new_file.seek (tell)


      return new_file



   def do_string (self, s, output = None, cascade_break = None):


      if self.KEEP_CASCADE:
         self.cascade = [s]


      for T in self.Translators:
         if cascade_break and self.Translators.index (T) >= cascade_break:
            break
         s = T.do_string (s) [0]
         if self.KEEP_CASCADE:
            self.cascade.append (s)

      if output in ('', None):
         return s

      return self._type_product (s, output)




   def save (self, file_name):

      """
         SE - A Python Stream Editor by Frederic Rentsch

            Version 2.3 

         SE.save (file_name)

            Writes its definitions to a compilable and editable text file.
            'file_name' may be a file object open for writing.

      """

      if type (file_name) == str:
         try: SEL.os.stat (file_name)
         except OSError: pass
         else:
            response = ' '
            while response [0] not in 'YyNn':
               response = raw_input ('Definition file %s exists. Overwrite? (y/n) > ' % file_name)
            if response [0] in 'Nn':
               response = raw_input ('Different file name? (Return exits) > ')
               if response: file_name = response
               else: return
         f = file (file_name, 'wa')
         owns_file = YES
      else:
         f = file_name
         owns_file = NO
      i = 0
      number_of_translators = len (self.Translators)
      while i < number_of_translators -1:
         self.Translators [i].save (f)
         f.write ('\n\n   |\n\n\n')
         i += 1
      self.Translators [-1].save (f)
      if owns_file:
         f.close ()





class Translator (SEL.Translator):


   """
      SE - A Python Stream Editor

         Version 2.3 

         by Frederic Rentsch
         (c) 2006

      SE and SE are freeware in exchange for authorship credit.

      ---------------------------------------------------------------------------------------------------------

      class SE.Translator

         A Translator object contains a set of substitutions and performs them on any input data returning
         the translation.

         One or more Translators reside in a list that is an attribute of a SE object. The output of each
         Translator in the list is the input of the next one.

      Methods:

         reverse (report_irreversibles = 0):
         show ()
         add (definitions)
         drop (*target_numbers)
         save (file_name)

   """


   def __init__ (self, TL = None):

       SEL.Translator.__init__ (self)

       if TL:
          if isinstance (TL, SEL.Translator):
             self.single_byte    = TL.single_byte
             self.single_byte_on = TL.single_byte_on
             self.multi_byte     = TL.multi_byte
             self.multi_byte_on  = TL.multi_byte_on
             self.hard_regex     = TL.hard_regex
             self.hard_regex_on  = TL.hard_regex_on
             self.soft_regex     = TL.soft_regex
             self.soft_regex_on  = TL.soft_regex_on
             self.NULL_MODE      = TL.NULL_MODE


   def reverse (self, report_irreversibles = NO):

      """
         SE - A Python Stream Editor by Frederic Rentsch

            Version 2.3 

         SE.Translator.reverse (report_irreversibles = 0)

            Returns a Translator with reversed definitions so that a translation made by self
            can be reversed with the Translator made by this method, provided all definitions
            are reversible. Irreversible definitions are: regular expressions, multiple targets
            with identical substitutes and deletions. 'report_irreversibles' set shows a list
            of all irreversible definitions.

      """

      grab = {}
      irreversibles = []
      show_count = 1

      for i in range (256):
         if self.single_byte [i] != None:
            s, file_name_flag = self.single_byte [i]
            t = chr (i)
            if file_name_flag or s == '':
               irreversibles.append ((show_count, t, s, file_name_flag))
            else:
               if grab.has_key (s):
                  grab [s].append ((show_count, t, file_name_flag))
               else:
                  grab [s] = [(show_count, t, file_name_flag)]
            show_count += 1

      for i in range (256):
         if self.multi_byte [i] != None:
            for t, s, file_name_flag in self.multi_byte [i]:
               if file_name_flag or s == '':
                  irreversibles.append ((show_count, t, s, file_name_flag))
               else:
                  if grab.has_key (s):
                     grab [s].append ((show_count, t, file_name_flag))
                  else:
                     grab [s] = [(show_count, t, file_name_flag)]

               show_count += 1

      for i in range (256):
         if self.hard_regex [i] != None:
            for item in self.hard_regex [i]:
               irreversibles.append ((show_count, item [0], item [2], item [4]))
               show_count += 1

      for item in self.soft_regex:
         irreversibles.append ((show_count, item [0], item [2], item [4]))
         show_count += 1

      definitions = ''

      for s in grab:

         targets = grab [s]

         do = YES
         if len (targets) == 1:
            if targets [0][0] == '':
               irreversibles.append ((targets [0][0], targets [0][1], s, targets [0][2]))
               do = NO

         else:
            for i in range (len (targets)):
               irreversibles.append ((targets [i][0], targets [i][1], s, targets [i][2]))
               do = NO

         if do:
            t = targets [0][1]
            if SEL._SC_TARGET in s:
               if SEL._SC_TARGET == SEL._SC_SEPARATOR:
                  d = '(%d)(%d)=(%d)(%d) %s%s=%s' % (ord (SEL._SC_LITERALIZER), ord (SEL._SC_TARGET), ord (SEL._SC_LITERALIZER), ord (SEL._SC_TARGET), SEL._SC_LITERALIZER, SEL._SC_TARGET, t)
                  S = SEL.SEL (d)
                  s = S (s)
               else:
                  s = s.replace (SEL._SC_TARGET, t)

            t = _substitute_translator_to_definition (t)
            s = _target_translator_to_definition (s)

            if SEL.re.search ('\s', s + t):
               definitions += '"%s=%s"\n' % (s, t)
            else:
               definitions += '%s=%s\n' % (s, t)

      if report_irreversibles and irreversibles:
         print 'Skipping irreversible definitions:'
         for show_count, t, s, file_name_flag in irreversibles:
            format = _formats [file_name_flag]
            print format % (show_count, _target_translator_to_display (t), _substitute_translator_to_display (s))

      T = Translator ()
      T.add (definitions)
      return T



   def _single_byte_definitions (self, show_count = None):
      show = ''
      for i in range (256):
         item = self.single_byte [i]
         if item != None:
            if show_count == None:
               format = _formats_no_count [item [1]]
               arguments = _target_translator_to_display (chr (i)), _substitute_translator_to_display (self.single_byte [i][0])
            else:
               format = _formats [item [1]]
               arguments = show_count, _target_translator_to_display (chr (i)), _substitute_translator_to_display (self.single_byte [i][0])
               show_count += 1
            show += format % arguments + '\n'
      return show, show_count

   def _multi_byte_definitions (self, show_count = None):
      show = ''
      for i in range (256):
         if self.multi_byte [i] != None:
            for item in self.multi_byte [i]:
               if show_count == None:
                  format = _formats_no_count [item [2]]
                  arguments = _target_translator_to_display (item [0]), _substitute_translator_to_display (item [1])
               else:
                  format = _formats [item [2]]
                  arguments = show_count, _target_translator_to_display (item [0]), _substitute_translator_to_display (item [1])
                  show_count += 1
               show += format % arguments + '\n'
      return show, show_count

   def _hard_re_definitions (self, show_count = None):
      show = ''
      for i in range (256):
         if self.hard_regex [i] != None:
            for item in self.hard_regex [i]:
               if show_count == None:
                  format = _formats_no_count [item [4]]
                  arguments = repr (item [0])[1:-1], _substitute_translator_to_display (item [2])
               else:
                  format = _formats [item [4]]
                  arguments = show_count, repr (item [0])[1:-1], _substitute_translator_to_display (item [2])
                  show_count += 1
               show += format % arguments + '\n'

      return show, show_count

   def _soft_re_definitions (self, show_count = None):
      show = ''
      for item in self.soft_regex:
         if show_count == None:
            format = _formats_no_count [item [4]]
            arguments = repr (item [0])[1:-1], _substitute_translator_to_display (item [2])
         else:
            format = _formats [item [4]]
            arguments = show_count, repr (item [0])[1:-1], _substitute_translator_to_display (item [2])
            show_count += 1
         show += format % arguments + '\n'
      return show, show_count



   def _all_definitions (self):

      """
         Returns an LF-separated string of all of the Translator's double-quoted definitions

      """

      show = ''
      if self.single_byte_on:
         show += self._single_byte_definitions ()[0]

      if self.multi_byte_on:
         show += self._multi_byte_definitions ()[0]

      if self.hard_regex_on:
         show += self._hard_re_definitions ()[0]

      if self.soft_regex_on:
         show += self._soft_re_definitions ()[0]
      return show



   def show (self):

      show_count = 1

      print 'NULL_MODE > %d (%s)' % (self.NULL_MODE, ('PASS: unmatched data passes', 'EAT: unmatched data does not pass') [self.NULL_MODE == SEL.EAT])

      if self.single_byte_on:
         print 'Single-Byte Targets'
         show, show_count = self._single_byte_definitions (show_count)
         print show

      if self.multi_byte_on:
         print 'Multi-Byte Targets'
         show, show_count = self._multi_byte_definitions (show_count)
         print show

      if self.hard_regex_on:
         print 'Hard Regex Targets'
         show, show_count = self._hard_re_definitions (show_count)
         print show

      if self.soft_regex_on:
         print 'Soft Regex Targets'
         show, show_count = self._soft_re_definitions (show_count)
         print show
      print




   def add (self, definitions):

      """
         SE - A Python Stream Editor by Frederic Rentsch

            Version 2.3 

         SE.Translator.add (substitution definitions)

            'substitution definitions' are a string containing definitions and / or file names.

      """

      if type (definitions) != str:
         self.log.append ('%s - Translator - Illegal argument type: %s' % (SEL.time.ctime (), repr (definitions)))
      else:
         Translators = [self]
         SC = SEL.Substitutions_Compiler (SEL.cStringIO.StringIO (definitions), Translator)
         SC (Translators)
         self.log.extend (SC.log)
         if len (Translators) > 1:
            self.log.append ('%s - Translator - Cannot add runs. Ignoring definitions past run symbol (\'%s\')'  % (time.ctime (), SEL._SC_RUN))
         self.activate_registers ()



   def drop (self, *target_numbers):

      """
         SE - A Python Stream Editor by Frederic Rentsch

            Version 2.3 

         SE.Translator.drop (*target_numbers)

            Method show () displays all definitions in a sequentially numbered list. The arguments
            'target numbers' refer to that list. The numbers do not identify definitions, but
            get reassigned after each addition or deletion. Calling drop () without argument
            displays the numbered list.
               Target numbers are either integers or sequences: (1,2,3,4,99) == (range (1,5),99)

      """

      numbers = []
      for item in target_numbers:
         if type (item) != int:
            numbers.extend (list (item))
         else:
            numbers.append (item)
      numbers.sort ()

      do_count = 0
      done = NO

      if self.single_byte_on:
         for i in range (256):
            if self.single_byte [i] != None:
               do_count += 1
               if do_count == numbers [0]:
                  self.single_byte [i] = None
                  numbers.pop (0)
                  if numbers == []:
                     done = YES
                     break

      if not done:

         delete_list = []
         if self.multi_byte_on:
            for i in range (256):
               if self.multi_byte [i] != None:
                  l = self.multi_byte [i]
                  j = 0
                  for item in l:
                     do_count += 1
                     if do_count == numbers [0]:
                        delete_list.append (j)
                        numbers.pop (0)
                        if numbers == []:
                           done = YES
                           break
                     j += 1
                  for item in reversed (delete_list):
                     del (l [item])

      if not done:

         if self.hard_regex_on:
            for i in range (256):
               if self.hard_regex [i] != None:
                  l = self.hard_regex [i]
                  j = 0
                  for item in l:
                     do_count += 1
                     if do_count == numbers [0]:
                        delete_list.append (j)
                        numbers.pop (0)
                        if numbers == []:
                           done = YES
                           break
                     j += 1
                  for item in reversed (delete_list):
                     del (l [item])

      if not done:

         if self.soft_regex_on:
            j = 0
            for item in self.soft_regex:
               do_count += 1
               if do_count == numbers [0]:
                  delete_list.append (j)
                  numbers.pop (0)
                  if numbers == []:
                     break
               j += 1
            for item in reversed (delete_list):
               del (l [item])


      self.activate_registers ()



   def drop_fixed_target (self, target):

      """
         SE - A Python Stream Editor by Frederic Rentsch

            Version 2.3 

         SE.Translator.drop_fixed_target (target)

            Method drop () drops by sequence numbers, because that is a much more convenient
            format to enter than a list of targets. Some function may need to drop defintions
            by target.
               This method does not drop regular expressions. Calling it with one will have
            no effect.

      """

      done = NO
      l = len (target)
      if l == 1:
         if self.single_byte_on:
            self.single_byte [ord (target)] = None
            done = YES
      else:
         if self.multi_byte_on:
            table = self.multi_byte [ord (target [0])]
            try: delete_index = table.index (target)
            except ValueError: pass
            else:
               del table [index][delete_index]
               done = YES
      if done:
         self.activate_registers ()




   def save (self, file_name):

      """
         SE - A Python Stream Editor by Frederic Rentsch

            Version 2.3 

         SE.Translator.save (file_name)

            Writes its definitions to a compilable and editable text file.

      """

      unquoted_format = ' %s=%s\n'
      quoted_format = ' %s%%s=%%s%s\n' % (SEL._SC_QUOTE, SEL._SC_QUOTE)
      unquoted_def_file_format = ' %%s=%s%%s%s\n' % (SEL._SC_FILE_NAME[0], SEL._SC_FILE_NAME[1])
      quoted_def_file_format = ' %s%%s=%s%%s%s%s\n' % (SEL._SC_QUOTE, SEL._SC_FILE_NAME[0], SEL._SC_FILE_NAME[1], SEL._SC_QUOTE)
      unquoted_re_format = ' %s%%s%s=%%s\n' % (SEL._SC_REGEX, SEL._SC_REGEX)
      quoted_re_format = ' %s%s%%s%s=%%s%s\n' % (SEL._SC_QUOTE, SEL._SC_REGEX, SEL._SC_REGEX, SEL._SC_QUOTE)
      unquoted_re_format_def_file_name = ' %s%%s%s=%s%%s%s\n' % (SEL._SC_REGEX, SEL._SC_REGEX, SEL._SC_FILE_NAME[0], SEL._SC_FILE_NAME[1])
      quoted_re_format_def_file_name = ' %s%s%%s%s=%s%%s%s%s\n' % (SEL._SC_QUOTE, SEL._SC_REGEX, SEL._SC_REGEX, SEL._SC_FILE_NAME[0], SEL._SC_FILE_NAME[1], SEL._SC_QUOTE)

      formats = (
         unquoted_format,
         quoted_format,
         unquoted_def_file_format,
         quoted_def_file_format,
         unquoted_re_format,
         quoted_re_format,
         unquoted_re_format_def_file_name,
         quoted_re_format_def_file_name, )

      def save_single_byte ():
         for i in range (256):
            if self.single_byte [i] != None:
               item = self.single_byte [i]
               target_c = _target_translator_to_definition (chr (i))
               any = _substitute_translator_to_definition (item [0])
               format_flag = 0
               if SEL.re.search ('\s', target_c + any):
                  format_flag = 1  # Quote
               if item [1]:
                  format_flag |= 2
               format = formats [format_flag]
               f.write (format % (target_c, any))

      def save_multi_byte ():
         for i in range (256):
            if self.multi_byte [i] != None:
               for item in self.multi_byte [i]:
                  item [1].replace (item [0], SEL._SC_TARGET)
                  many = _target_translator_to_definition (item [0])
                  format_flag = 0
                  any = _substitute_translator_to_definition (item [1])
                  if SEL.re.search ('\s', many + any):
                     format_flag = 1  # Quote
                  if item [2]:
                     format_flag |= 2
                  format = formats [format_flag]
                  f.write (format % (many, any))

      def save_hard_re ():
         for i in range (256):
            if self.hard_regex [i] != None:
               for item in self.hard_regex [i]:
                  t = _visualize_re (item [0])
                  s = _substitute_translator_to_definition (item [2])
                  format_flag = 4
                  if SEL.re.search ('\s', t + s):
                     format_flag |= 1  # Quote
                  if item [4]:
                     format_flag |= 2
                  format = formats [format_flag]
                  f.write (format % (t, s))

      def save_soft_re ():
         for item in self.soft_regex:
             t = _visualize_re (item [0])
             s = _substitute_translator_to_definition (item [2])
             format_flag = 4
             if SEL.re.search ('\s', t + s):
                format_flag |= 1  # Quote
             if item [4]:
                format_flag |= 2
             format = formats [format_flag]
             f.write (format % (t, s))

      if type (file_name) == str:
         try: SEL.os.stat (file_name)
         except OSError: pass
         else:
            response = ' '
            while response [0] not in 'YyNn':
               response = raw_input ('Definition file %s exists. Overwrite? (y/n) > ' % file_name)
            if response [0] in 'Nn':
               response = raw_input ('Different file name? (Return exits) > ')
               if response: file_name = response
               else: return
         f = file (file_name, 'wa')
         owns_file = YES
      else:
         f = file_name
         owns_file = NO

      f.write ('# SE Defintions %s\n# %s\n\n' % (SEL.time.ctime (), f.name))


      if self.NULL_MODE == SEL.EAT:
         f.write ('%s\n' % SEL._EATALL_KEYWORD)

      f.write ('\n\n# Single-Byte Targets\n\n')
      if self.single_byte_on:
         save_single_byte ()

      f.write ('\n\n# Multi-Byte Targets\n\n')
      if self.multi_byte_on:
         save_multi_byte ()

      f.write ('\n\n# Hard Regex Targets\n\n')
      if self.hard_regex_on:
         save_hard_re ()

      f.write ('\n\n# Soft Regex Targets\n\n')
      if self.soft_regex_on:
         save_soft_re ()

      if owns_file:
            f.close ()




##################################


# Spaces prompt double-quoting the whole definition and so are not special.



def _char_to_ascii (c):
   ord_c = ord (c)
   if 0 <= ord_c <= 31 or ord_c in (128, 160, 255):
      return '(x%02x)' % ord_c
   else:
      return c



def _translator_to_definition (x, initials, specials):

   if x == '': return x

   x_ = ''
   l = len (x)
   c = x [0]

   if c in initials:
      x_ = SEL._SC_LITERALIZER
   else:
      if c == SEL._SC_ASCII_ESCAPE:
         cc, ii = SEL._do_ascii (x, 0, l)
         if ii > 0:   # is ascii
            x_ = SEL._SC_LITERALIZER

   x_ += _char_to_ascii (x [0])


   i = 1
   while i < l:
      c = x [i]
      if c in specials:
         x_ += SEL._SC_LITERALIZER

      elif c == SEL._SC_ASCII_ESCAPE:
         cc, ii = SEL._do_ascii (x, i, l)
         if ii != i:
            x_ += SEL._SC_LITERALIZER
      else:
         c_ = _char_to_ascii (c)
         if c != c_:
            c = c_
      x_ += c
      i += 1


   return x_




def _target_translator_to_definition (t):

   return _translator_to_definition (t, SEL._TAS_INITIALS, SEL._TAS_SPECIALS)



def _substitute_translator_to_definition (s):

   return _translator_to_definition (s, SEL._SUS_INITIALS, SEL._SUS_SPECIALS)




##################################




def _target_translator_to_display (t):

   return _translator_to_definition (t, SEL._TAD_INITIALS, SEL._TAD_SPECIALS)



def _substitute_translator_to_display (s):

   return _translator_to_definition (s, SEL._SUD_INITIALS, SEL._SUD_SPECIALS)




# Regular and file name substitute display formats

_formats          = '%5d: |%s|->|%s|', '%%5d: |%%s|->|%s%%s%s|' % (SEL._SC_FILE_NAME [0], SEL._SC_FILE_NAME [1])

_formats_no_count = '"%s=%s"', '"%%s=%s%%s%s"' % (SEL._SC_FILE_NAME [0], SEL._SC_FILE_NAME [1])




def _visualize_re (s):

   '''Visualizes unprintable ascii codes by replacing them with escaped characters'''

   vs = ''
   i = 0
   for c in s:
      ord_c = ord (c)
      if ord_c <= 31 or ord_c == 128:
         vs += '\\x%02x' % ord_c
      else:
         vs += c
      i += 1
   return vs





####################################################
#
#
# 6/20/2006 2:56PM  (c) 2006 Frederic Rentsch
#
#
#####################################################

