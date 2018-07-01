# SEL.PY

# Version 2.3


"""
   SEL - A Python Stream Editor

   Version 2.3 

   by Frederic Rentsch
   (c) 2006

   SE and SEL are freeware in exchange for authorship credit.

   ------------------------------------------------------------------------------

   SEL stands for SE 'Light'. SEL is the functional component of SE and does not
   have its facilities for interactive development.
      If interaction is not required, importing SEL loads no more than is necessary.

   More ot the Editor Class:
      SEL.SEL.__doc__
      SEL.SEL.__call__.__doc__

   Read all about it in SE-DOC.HTM

"""

__version__ = "2.3"
__author__ = "Frederic Rentsch (anthra.norell@vtxmail.ch)"
__copyright__ = "(C) 2006. Frederic Rentsch"


import sys, os, re, time, cStringIO


def version ():  return 'SEL 2.3'




############################################################

# Null-edit modes eat and pass

PASS        = 0
EAT         = 1

_PASSALL_KEYWORD = '<PASS>'
_EATALL_KEYWORD  = '<EAT>'

_modes = { '<PASS>' : PASS, '<EAT>' : EAT  }




############################################################

# Internals

OK  = 1
NOT_OK = not OK

NO  = 0
YES = 1

_MAX_FILE_NAME_LENGTH =  256
_BINARY_SEARCH_THRESHOLD = 10

_AUTO_DETECT = 0
_STRING      = 1
_FILE        = 2
_FILE_NAME   = 3

_FIXED_PRECEDENCE     =  2    # Higher precedence
_REGEX_PRECEDENCE     =  1
_TEMP_FILE_PREFIX     = '~'
_AUTO_EXTENSION       = '.~se'




############################################################

# Special characters in definitions

_SC_QUOTE           = '"'
_SC_COMMENT         = '#'
_SC_SEPARATOR       = '='
_SC_TARGET          = _SC_SEPARATOR
_SC_ASCII           = '()'
_SC_LITERALIZER     = '\\'
_SC_RUN             = '|'
_SC_REGEX           = '~'
_SC_FILE_NAME       = '<>'  # File name starts with this ((not a legal file name character)
_SC_SPACES          = ' \t\r\n\l\v'

_MAX_TARGET_LENGTH  = 1024
_INPUT_PATH         = \
_OUTPUT_PATH        = None
_BACKUP_EXTENSION   = '.bak'

_LOCKED     = 0
_APPEND     = 1     # Append
_OVERWRITE  = 2     # Allow replace file name
_IN_PLACE   = 3     # Default out file name is in file name


_SC_ASCII_ESCAPE = _SC_ASCII [0]   # Contingent on valid ascii value


# Target compile special characters:
#   These characters need a literalizer deleted when compiled

_TAC_INITIALS     = _SC_QUOTE + _SC_COMMENT + _SC_SEPARATOR + _SC_REGEX # + _SC_LITERALIZER
_TAC_SPECIALS     = _SC_SEPARATOR # + _SC_LITERALIZER


# Substitute compile special characters:
#   These characters need a literalizer deleted when compiled

_SUC_INITIALS     = _SC_QUOTE + _SC_FILE_NAME [0]
_SUC_SPECIALS     = _SC_QUOTE


# Target Display special characters:
#   These characters require a literalizer when displayed

_TAD_INITIALS     = ''
_TAD_SPECIALS     = ''


# Substitute Display special characters:
#   These characters require a literalizer when displayed

_SUD_INITIALS     = _SC_FILE_NAME [0]
_SUD_SPECIALS     = '' # _SC_LITERALIZER


# Target save special characters:
#   These characters require a literalizer when saved to a compilable file

_TAS_INITIALS     = _SC_QUOTE + _SC_COMMENT + _SC_REGEX + _SC_SEPARATOR # + _SC_LITERALIZER
_TAS_SPECIALS     = _SC_QUOTE + _SC_SEPARATOR # + _SC_LITERALIZER


# Substitute save special characters:
#   These characters require a literalizer when saved to a compilable file

_SUS_INITIALS     = _SC_QUOTE + _SC_FILE_NAME # + _SC_LITERALIZER
_SUS_SPECIALS     = _SC_QUOTE # + _SC_LITERALIZER


########################################################


_is_regex = re.compile (r'~(.|\n)*?[^\\]~=')

_is_fixed = re.compile (r'(.|\n)*?[^\\]=')


########################################################

#
# If by mistake the definition compiler is given a file
# that is not a defintions file, it is bound to report
# an endless series of uncompilable words. The dud
# limiter stops at this limit and prompts for either
# continuation or termination.

_dud_counter          =    0
_DUD_LIMITER          =   10

########################################################

# Default path for definition files


DEFINITION_PATH = None


def set (reset = NO, definition_path = None):

   global DEFINITION_PATH
   if definition_path != None:
      if definition_path [-1] != '/':
         definition_path += '/'
         DEFINITION_PATH = definition_path
   elif reset:
      DEFINITION_PATH = None


########################################################



class SEL:

   """
      SEL - A Python Stream Editor

      Version 2.3 

      by Frederic Rentsch
      (c) 2006

      SE and SEL are freeware in exchange for authorship credit.

      ------------------------------------------------------------------------------

      SEL is the functional component of SE and offers no interactive facilities.
      If interaction or directions are desired, use SE.

   """

   MAX_TARGET_LENGTH  = _MAX_TARGET_LENGTH

   INPUT_PATH         = _INPUT_PATH
   OUTPUT_PATH        = _OUTPUT_PATH
   FILE_HANDLING_FLAG = _LOCKED           # All names of exisiting data files are protected
   BACKUP_EXTENSION   = _BACKUP_EXTENSION

   Translator_Class   = None
   Translators        = None              # Translation engines, one per substitution set

   _out_file_name     = None              # Hold for cascade display

   _recursion_count   = 0                 # For renaming backups

   log                = None


   def __init__ (self, substitutions, file_handling_flag = NO, Translator_Class = None):


      if Translator_Class == None:
         self.Translator_Class = Translator
      else:
         self.Translator_Class = Translator_Class

      if file_handling_flag:
         self.FILE_HANDLING_FLAG = file_handling_flag

      self.log = []
      SC = Substitutions_Compiler (cStringIO.StringIO (substitutions), self.Translator_Class)
      self.Translators = [self.Translator_Class ()]
      SC (self.Translators)
      self.log.extend (SC.log)
      delete_list = []
      for T in self.Translators:
         number_of_modes = T.activate_registers ()
         delete_list.append (number_of_modes == 0)
      i = len (delete_list)
      while i > 1:
         i -= 1
         if delete_list [i]:
            del self.Translators [i]



   def set (self, reset = NO,
            input_path         = None,
            output_path        = None,
            file_handling_flag = None,
            max_target_length  = None,
            backup_extension   = None):
      
      if input_path != None:
         if not input_path [-1] in ':/': input_path += '/'
         self.INPUT_PATH = input_path
      elif reset:
         self.INPUT_PATH = _INPUT_PATH

      if output_path != None:
         if not output_path [-1] in ':/': output_path += '/'
         self.OUTPUT_PATH = output_path
      elif reset:
         self.OUTPUT_PATH = _OUTPUT_PATH

      if file_handling_flag != None:
         self.FILE_HANDLING_FLAG = file_handling_flag
      elif reset:
         self.FILE_HANDLING_FLAG = _LOCKED

      if backup_extension != None:
         self.BACKUP_EXTENSION = backup_extension
      elif reset:
         self.BACKUP_EXTENSION = _BACKUP_EXTENSION

      if max_target_length != None:
         self.MAX_TARGET_LENGTH = max_target_length
      elif reset:
         self.MAX_TARGET_LENGTH = _MAX_TARGET_LENGTH



   def __call__ (self, input, output = None, cascade_break = None):

      in_type = type (input)

      if type (output) == file:
         name = output.name
         output.flush ()
         output.seek (output.tell ())

      elif output and type (output) == str:
         name = output

      else:
         name = None

      if name != None:
         p, n = os.path.split (name)
         if p == '':
            if self.OUTPUT_PATH:
               output = name = self.OUTPUT_PATH + name

      self._out_file_name = name

      if in_type == file:
         return self.do_file (input, output)

      if in_type != str:
         self.log.append ('%s - Editor - Illegal argument type: %s' % (time.ctime (), repr (input)))
         return

      len_input = len (input)
      if len_input > _MAX_FILE_NAME_LENGTH:
         in_type = _STRING

      stripped_input = input.strip ()

      if len (stripped_input) < len_input:
         in_type = _STRING

      else:

         tentative_in_file_name = input

         in_path, name = os.path.split (tentative_in_file_name)

         if name == '':
            in_type = _STRING
         else:
            if in_path == '':
               if self.INPUT_PATH:
                  in_path = self.INPUT_PATH
               tentative_in_file_name = in_path + tentative_in_file_name

            else:
               if in_path [-1] not in ':/\\':
                  in_path += '/'

            in_type = _STRING
            try:
               os.stat (tentative_in_file_name)
               in_type = _FILE_NAME
            except:
               pass

      if in_type == _STRING:
         return self.do_string (input, output, cascade_break)

      if in_type == _FILE_NAME:
         return self.do_file_name (tentative_in_file_name, output, cascade_break)

      self.log.append ('%s - Editor - Unknown source-stream type: %s, %s' % (time.ctime (), repr (in_type), input.__class__))



   def _type_product (self, product, output, keep_temp = NO):


      """
         SEL.SEL._type_product (product, output)

            product is either a string or a file object
            output is either, None, '', a file name or a file

      """

      def rename_backup_files (file_name):

         if file_name == None:
            return None

         backup_name = file_name + self.BACKUP_EXTENSION

         try:
            os.rename (file_name, backup_name)
         except OSError, (errno, stderr):
            if errno != 17:
               self.log.append ('%s - Editor -  OS error: %s: %s\n' % (time.ctime (), stderr, file_name))
               return product
            self._recursion_count += 1
            return rename_backup_files (backup_name)
         else:
            self._recursion_count -= 1
            if self._recursion_count == -1:
               return file_name
            previous_file_name = file_name [:file_name.rindex (self.BACKUP_EXTENSION)]
            return rename_backup_files (previous_file_name)

      product_type = type (product)
      product_name = None
      product_string = None

      if product_type == file:
         product_type = _FILE
         product_name = product.name
         product.seek (0)

      elif product_type == str:
         product_type = _STRING
         product_string = product
         product = cStringIO.StringIO (product_string)

      else:
         self.log.append ('%s - Editor - Unknown product type %s: %s\n' % (time.ctime (), repr (product), type (product)))
         out_type = type (product)

      if type (output) == file:
         out_type = _FILE
      elif output == '':
         out_type = _STRING
      elif type (output) == str:
         out_type = _FILE_NAME
      elif output == None:
         out_type = product_type
      else:
         self.log.append ('%s - Editor - Unknown output type %s\n' % repr (time.ctime (), output))
         return

      if out_type == _FILE_NAME:

         try:
            os.stat (output)

         except OSError:    # File does not exist

            if product_type == _FILE:
               product.close ()
               os.rename (product_name, output)
            else:
               f = file (output, 'w+b')
               f.write (product.read ())
               f.close ()
               product.close ()
            return output

         else:    # file exists

            out_path = os.path.split (output) [0]
            if out_path == '':
               if self.OUTPUT_PATH:
                  out_path = self.OUTPUT_PATH
            else:
               if not out_path [-1] in ':/\\':
                  out_path += '/'

            if product_name == None:   # Product is string
               product_name = out_path + _TEMP_FILE_PREFIX + _time_code () [1:] + _AUTO_EXTENSION
               f = file (product_name, 'wb')
               f.write (product.read ())
               f.close ()

            go_ahead = self.FILE_HANDLING_FLAG != _LOCKED

            if not go_ahead:
               self.log.append ('%s - Editor - Don\'t have permission to change file \'%s\'. Translated file is \'%s\'.' % (time.ctime (), output, product_name))
               output = product_name
               keep_temp = YES

            else:

               if self.FILE_HANDLING_FLAG == _APPEND:
                  f = file (output, 'a+b')
                  f.write (product.read ())
                  f.close ()

               elif self.FILE_HANDLING_FLAG & _OVERWRITE:
                  try:
                     os.stat (output)
                  except OSError:
                     pass
                  else:
                     backup_name = output + self.BACKUP_EXTENSION
                     self._recursion_count = 0
                     discard = rename_backup_files (output)

                  if product_type == _STRING:
                     f = file (output, 'wb')
                     product.seek (0)
                     f.write (product.read ())
                     f.close ()

                  else:
                     try:
                        product.close ()
                        os.rename (product.name, output)
                     except OSError, (errno, stderr):
                        if errno == 13:
                           self.log.append ('%s - Editor - File %s seems to be locked. Cannot rename.' % (time.ctime (), output))
                           return product.name
                  product.close ()

            return output

      elif out_type == _STRING:
         output = product.read ()

      else:   # is _FILE

         if output == None:
            out_path = os.path.split (product_name) [0]
            if out_path == '':
               if self.OUTPUT_PATH:
                  out_path = self.OUTPUT_PATH
            if product_type == file: file_mode = product.mode
            else: file_mode = 'w+b'
            output = file (os.path.join (out_path, out_path + _TEMP_FILE_PREFIX + _time_code () [1:] + _AUTO_EXTENSION), file_mode)

         try:
            output.write (product.read ())
            output.flush ()
            output.seek (output.tell ())

         except (ValueError, IOError, OSError):
            m = 'Cannot write to file object %s. Returning ' % output.name
            if product_type == _STRING:
               m += 'string'
               output = product_string
            else:
               m += '%s' % product.name
               output = file (product.name, 'a+b')
               output.seek (0, 2)
            self.log.append ('%s - Editor - %s' % (time.ctime (), m))

      if not keep_temp and product_type == _FILE:
         product.close ()
         os.remove (product.name)

      return output



   def do_file_name (self, in_file_name, output = None, cascade_break = None):

      """
         in_file_name is final pathwise

      """

      try: in_file = file (in_file_name, 'rb')
      except:
         self.log.append ('%s - Editor - Cannot open file %s' % (time.ctime (), in_file_name))
         return

      input_path, input_name = os.path.split (in_file_name)

      if input_path and input_path [-1] not in '\\/':
         input_path += '/'
      if input_path == '' and self.INPUT_PATH:
         input_name = self.INPUT_PATH + input_name

      if output == None:
         if self.OUTPUT_PATH:
            output_path = self.OUTPUT_PATH
            output = output_path + input_name
         else:
            output = in_file_name
            output_path = input_path
         if self.FILE_HANDLING_FLAG != _IN_PLACE:
            output += _AUTO_EXTENSION
      elif type (output) == str:
         if output != '':
            output_path, out_file_name = os.path.split (output)
            if output_path == '':
               if self.OUTPUT_PATH != None:
                  output = self.OUTPUT_PATH + out_file_name
               elif input_path:
                  output = input_path + out_file_name
         else:
            output_path = self.OUTPUT_PATH
      else:   # file type
         output_path, out_file_name = os.path.split (output)
         if output_path == '':
            if self.OUTPUT_PATH != None:
               output = self.OUTPUT_PATH + out_file_name
            elif input_path:
               output = input_path + out_file_name

      out_file = self._do_file (in_file, output_path)
      in_file.close ()

      output = self._type_product (out_file, output)

      return output




   def do_file (self, in_file, output = None, cascade_break = None):


      """
         SEL.SEL.do_file (in_file, output = None)

            in_file is a file open for reading.
            output: None = same type, '' = string, string = file name, file object

      """

      out_file_path = self.OUTPUT_PATH

      if type (output) == str and output > '':
         out_file_path, out_file_name = os.path.split (output)
         if not out_file_path:
            if self.OUTPUT_PATH == None:
               in_file_path, in_file_name = os.path.split (in_file.name)
               if in_file_path:
                  out_file_path = in_file_path
         if out_file_path and not out_file_path [-1] in ':/\\':
            out_file_path += '/'
         output = out_file_path + out_file_name

      product = self._do_file (in_file, out_file_path)

      output = self._type_product (product, output)

      return output




   def _do_file (self, in_file, out_file_path):

      new_file = self.Translators [0].do_file (in_file, out_file_path, self.MAX_TARGET_LENGTH)

      for T in self.Translators [1:]:
         new_file.seek (0)
         newest_file = T.do_file (new_file, out_file_path, self.MAX_TARGET_LENGTH)
         new_file.close ()
         os.remove (new_file.name)
         new_file = newest_file

      return new_file




   def do_string (self, s, output = None, cascade_break = None):


      """
         SEL.SEL.do_string ()
            output: None = stdout, 0 = same type, '' = string, string = file name, file object

      """

      for T in self.Translators:
         s = T.do_string (s) [0]

      if output in ('', None):
         return s

      return self._type_product (s, output)



   def show_log (self, show_translators = NO):

      if self.log:
         print
         for item in self.log:
            print item
         print
      if show_translators:
         for T in self.Translators:
            T.show_log ()




##########################################


# Global for _finalize_substitute () to report to Translator


_no_such_file = None





def _finalize_substitute (target, substitute, substitute_file_flag):

   """
      A substitute may be a file name or contain target place holders literal or symbolic.
      A file needs to be read and target place holders interpreted

   """

   global _no_such_file

   _no_such_file = None


   if substitute == None:
      return

   if substitute_file_flag:
      try:
         f = file (substitute, 'rb')
         substitute = f.read ()
         f.close ()
      except:
         _no_such_file = substitute
         return target
      return substitute

   if not '\\=' in substitute:
      return substitute.replace ('=', target)

   s_list = list (substitute)
   action_indexes = []
   DELETE = 1
   TARGET = 2
   literalized = NO
   i = target_index = 0
   l = len (s_list)
   while i < l:
      c = s_list [i]
      if c == _SC_LITERALIZER:
         literalized = YES
      elif c == _SC_TARGET:
         if not literalized:
            action_indexes.append ((i, TARGET))
         else:
            action_indexes.append ((i-1, DELETE))
         literalized = NO
      i += 1

   for i, action in reversed (action_indexes):
      if action == DELETE:
         del (s_list [i])
      elif action == TARGET:
         s_list [i] = target


   return ''.join (s_list)





class _translation_table (list):



   def __init__ (self):

      list.__init__ (self, 256 * [None])



   def unregister (self, target_character):

      self [ord (target_character)] = None





class single_byte (_translation_table):



   def register (self, target, substitute, substitute_file_flag):

      if len (target) == 1:
         self [ord (target)] = substitute, substitute_file_flag
      else:
         self.log.append ('%s - Compiler - Substitute \'%s\' has no target' % (time.ctime (), substitute))



   def return_substitute (self, stream):

      t = stream [0]
      s_c = self [ord (t)]

      if s_c != None:
         return _finalize_substitute (t, s_c [0], s_c [1])






class _multi_byte (_translation_table):


   def register (self, target, substitute, substitute_file_flag):

      table_i = ord (target [0])

      if self [table_i] == None:
         self [table_i] = []
         i = 0
         found = NO
      else:
         i, found = _binary_search (target, self [ord (target [0])], _comparison_function)

      if found:
         self [table_i][i] = (target, substitute, substitute_file_flag)
      else:
         self [table_i].insert (i, (target, substitute, substitute_file_flag))



   def unregister (self, target):

      ord_initial = ord (target [0])
      i, found = _binary_search (target, self [ord_initial], _comparison_function)
      if found: del self [ord_initial][i]




class multi_byte (_multi_byte):


   def return_substitute (self, stream):

      l = self [ord (stream [0])]
      if not l: return

      if len (l) < _BINARY_SEARCH_THRESHOLD:

         len_target = 1   # If not found.
         last_match = None
         number_of_items = len (l)
         i = 0
         while i < number_of_items:
            t, s, substitute_file_flag = l [i]
            if t == stream [:len (t)]:
               last_match = t, s, substitute_file_flag
            elif t > stream:
               break
            i += 1
         if last_match:
            t, s, substitute_file_flag = last_match
            return len (t), _FIXED_PRECEDENCE, 1, t, _finalize_substitute (t, s, substitute_file_flag)

      else:

         i, found = _binary_search (stream, l, _comparison_function)

         i -= found == 0

         while i >= 0:
            t, s, substitute_file_flag = l [i]
            len_target = len (t)
            data = stream [:len_target]
            if data == t:
               return len_target, _FIXED_PRECEDENCE, 1, t, _finalize_substitute (t, s, substitute_file_flag)
            elif data < t:
               break
            i -= 1



class hard_regex (multi_byte):


   def register (self, target, substitute, regex_count, substitute_file_flag):

      regex_special_characters = '(.?+*[|$^'

      target = target.replace ('"', '\\x22')

      if target [-1] != '\\':
         target = eval ("'''%s'''" % target)

      i = ord (target [0])

      if i == 92:  # ord ('\\')
         if target [1] in regex_special_characters:
            i = ord (target [1])

      if self [i] == None:
         self [i] = soft_regex ()

      self [i].register (target, substitute, regex_count, substitute_file_flag)



   def unregister (self, target):

      self [ord (target [0])].unregister (target)



   def return_substitute (self, stream):


      l = self [ord (stream [0])]

      if not l: return

      hits = []

      number_of_items = len (l)
      i = 0
      while i < number_of_items:
         l_i = l [i]
         match_object = l_i[1].match (stream)

         if match_object:
            match = match_object.group ()
            pattern              = l_i [0]
            substitute           = l_i [2]
            definition_order     = l_i [3]
            substitute_file_flag = l_i [4]
            hits.append ((len (match), _REGEX_PRECEDENCE, definition_order, match, substitute, pattern, substitute_file_flag))
         i += 1
      if hits:
         hits.sort ()
         hit = hits [-1]
         if hit [0] == 0:
            return

         substitute = _finalize_substitute (hit [3], hit [4], hit [6])

         return hit [:4] + (substitute,)




class soft_regex (list):


   def register (self, target, substitute, regex_count, substitute_file_flag):


      target_re = re.compile (target)

      i, found = _binary_search (target, self, _comparison_function)
      if found:
         self [i] = target, target_re, substitute, regex_count, substitute_file_flag
      else:
         self.insert (i, (target, target_re, substitute, regex_count, substitute_file_flag))



   def unregister (self, target):

      ord_initial = ord (target [0])
      i, found = _binary_search (target, self, _comparison_function)
      if found: self [i-1] = []



   def return_substitute (self, stream):

      hits = []
      for i in range (len (self)):
         l_i = self [i]
         match_object = l_i [1].match (stream)
         if match_object:
            match = match_object.group ()
            pattern              = l_i [0]
            substitute           = l_i [2]
            definition_order     = l_i [3]
            substitute_file_flag = l_i [4]
            hits.append ((len (match), _REGEX_PRECEDENCE, definition_order, match, substitute, pattern, substitute_file_flag))

      if hits:
         hits.sort ()
         hit = hits [-1]
         if hit [0] == 0:
            return

         substitute = _finalize_substitute (hit [3], hit [4], hit [6])

         return hit [0:4] + (substitute,)




########################################################




class Translator:


   single_byte      = None
   single_byte_on   = NO

   multi_byte       = None
   multi_byte_on    = NO

   hard_regex       = None
   hard_regex_on    = NO

   soft_regex       = None
   soft_regex_on    = NO

   NULL_MODE        = PASS

   _regex_count     = 0

   log              = None


   def __init__ (self):

      self.single_byte  = single_byte ()
      self.multi_byte   = multi_byte ()
      self.hard_regex   = hard_regex ()
      self.soft_regex   = soft_regex ()
      self.log          = []


   def set (self, reset = NO, null_mode = None):

      if filter_mode != None:
         self.NULL_MODE = null_mode
      elif reset:
         self.NULL_MODE = PASS



   def do_string (self, s, l = None):

      #  SEL.Translator.do_string (s, l = None)
      #     Doesn't care how long the string is. Memory overflow is the user's problem.
      #     The argument 'l' says how far the translation should go, so that the method
      #     do_buffer () can call this method. do_buffer () says how far the processing
      #     should go, because it cycles data through a buffer twice the maximum target
      #     length, advancing the read buffer by the maximum target length, which is only
      #     half of the buffer size.
      #     Returns a string.

      global _no_such_file


      new_s = ''

      i = 0
      if l == None:
         l = len (s)

      if not self.hard_regex_on and not self.soft_regex_on:

         while i < l:

            input = s [i:]
            initial = input [0]
            substitute = None
            move = 1
            done = NO

            if self.multi_byte_on:
               x = self.multi_byte.return_substitute (input)
               if x != None:     # len_target, _FIXED_PRECEDENCE precedence), 1, t, _finalize_substitute (t, s)
                  move, substitute = x [0], x [-1]
                  done = YES
            if not done:
               if self.single_byte_on:
                  substitute = self.single_byte.return_substitute (initial)
            if substitute != None:
               new_s += substitute
            else:
               if self.NULL_MODE == PASS:
                  new_s += initial

            if _no_such_file:
               self.log.append ('%s - Translator - No such substitute file: %s' % (time.ctime (), _no_such_file))

            i += move

         return new_s, i

      else:

         while i < l:

            input = s [i:]
            initial = input [0]
            substitute = None
            move = 1
            done = NO
            ranks = []

            if self.multi_byte_on:
               x = self.multi_byte.return_substitute (input)
               if x != None:
                  ranks.append (x)
                  done = YES

            if not done:
               if self.single_byte_on:
                  substitute = self.single_byte.return_substitute (initial)
                  if substitute != None:
                     ranks.append ((1, _FIXED_PRECEDENCE, 1, initial, substitute))
                     done = YES

            if self.hard_regex_on:
               x = self.hard_regex.return_substitute (input)

               if x != None:
                  ranks.append (x)
                  done = YES

            if self.soft_regex_on:
               x = self.soft_regex.return_substitute (input)
               if x != None:
                  ranks.append (x)
                  done = YES

            if done:
               ranks.sort ()
               l_cat_ord_t_s = ranks [-1]        # [(3, 1, 0, 'abc', 'fixed'), (3, 2, 1, 'abc', 're')]
               move, substitute = l_cat_ord_t_s [0], l_cat_ord_t_s [-1]
               try: new_s += substitute
               except TypeError: pass
            else:
               if self.NULL_MODE == PASS:
                  new_s += initial

            if _no_such_file:
               self.log.append ('%s - Translator - No such substitute file: %s' % (time.ctime (), _no_such_file))

            i += move

         return new_s, i




   def _do_buffer (self, b):

      """
         SEL.Translator._do_buffer (b)
            Cycles data through a buffer twice the maximum target length, advancing the
            read buffer by the maximim target length, which is half of the buffer size.
            Falls back on the method do_string ().
            Caller is responsible for passing a buffer whose length is an even number.
      """

      return self.do_string (b, len (b) / 2)



   def do_file (self, in_file, out_file_path, max_target_length):

      """
         SEL.Translator.do_file (in_file, out_file_path, max_target_length).
            in_file:  an open read file
            returns a self-made read-write file, open and flushed

      """

      in_file.flush ()

      out_file_name = out_file_path or ''
      out_file_name += '%s%s' % (_TEMP_FILE_PREFIX, _time_code ()[4:])  # [4:] cycles per month

      out_file = file (out_file_name, 'w+b')

      while 1:

         in_buffer = in_file.read (max_target_length * 2)
         bytes_read = len (in_buffer)

         if bytes_read == 0:
            break

         if bytes_read < max_target_length * 2:
            out_file.write (self.do_string (in_buffer) [0])
            break
         processed, moved = self._do_buffer (in_buffer)
         out_file.write (processed)
         in_file.seek (moved - bytes_read, 1)

      out_file.flush ()
      out_file.seek (out_file.tell ())

      return out_file



   def add_definition (self, target, substitute):


      category = _IS_DEFINITION

      l = len (target)


      if l > 1:

         if l > 2 and target [0] == _SC_REGEX and target [-1] == _SC_REGEX:

            target = target [1:-1]


            if target == '':
               return NOT_OK

            if target [0] == '^':
               target = target [1:]


            if target == '':
               return NOT_OK


            category |= _IS_REGEX

            first_letter = target [0]
            second_letter = target [1]
            l = len (target)
            is_soft = NO

            if first_letter in '.[(':
               category |= _IS_SOFT_REGEX
               is_soft = YES

            if l >= 2:

               if not is_soft:
                  soft_index = 1
                  if first_letter == '\\':
                     if second_letter in 'dDsSwW':
                        category |= _IS_SOFT_REGEX
                        is_soft = YES
                     elif len (eval ("r'''%s'''" % target [:2])) == 1:
                        soft_index = 2
                  if not is_soft:
                     if target [soft_index] in '?*|':
                        category |= _IS_SOFT_REGEX
                        is_soft = YES

      # substitute

      if substitute > '':
         if substitute [0] + substitute [-1] == _SC_FILE_NAME:
            substitute = substitute [1:-1]
            category |= _IS_SUBSTITUTE_FILE

      if category & _IS_REGEX:
         formated_target = target

      else:
         formated_target = _target_definition_to_translator (target)
         l = len (formated_target)
         if l == 1:
            category |= _IS_SINGLE_BYTE
         else:
            category |= _IS_MULTI_BYTE


      formated_substitute = _substitute_definition_to_translator (substitute)


      category_no_file_sub = category & ~_IS_SUBSTITUTE_FILE
      substitute_file_flag = category & _IS_SUBSTITUTE_FILE == _IS_SUBSTITUTE_FILE


      if category_no_file_sub == _SINGLE_BYTE:
         self._add_single_byte (formated_target, formated_substitute, substitute_file_flag)
      elif category_no_file_sub == _MULTI_BYTE:
         self._add_multi_byte (formated_target, formated_substitute, substitute_file_flag)
      elif category_no_file_sub == _HARD_REGEX:
         self._add_hard_re (formated_target, formated_substitute, substitute_file_flag)
      elif category_no_file_sub == _SOFT_REGEX:
         self._add_soft_re (formated_target, formated_substitute, substitute_file_flag)

      return OK



   def _add_single_byte (self, target, substitute, substitute_file_flag):

      self.single_byte.register (target, substitute, substitute_file_flag)



   def _add_multi_byte (self, target, substitute, substitute_file_flag):

      self.multi_byte.register (target, substitute, substitute_file_flag)



   def _add_hard_re (self, target, substitute, substitute_file_flag):

      self._regex_count += 1
      self.hard_regex.register (target, substitute, self._regex_count, substitute_file_flag)



   def _add_soft_re (self, target, substitute, substitute_file_flag):

      self._regex_count += 1
      self.soft_regex.register (target, substitute, self._regex_count, substitute_file_flag)



   def activate_registers (self):

      self.single_byte_on  = self.single_byte.count (None) < 256
      self.multi_byte_on = self.multi_byte.count (None) < 256
      self.hard_regex_on = self.hard_regex.count (None) < 256
      self.soft_regex_on = len (self.soft_regex) > 0
      return self.single_byte_on + self.multi_byte_on + self.hard_regex_on + self.soft_regex_on


   def show_log (self):
      if self.log:
         print
         for item in self.log:
            print item
         print



#########################################################

# Special characters and literalizer


def _process_literalizers (s, initials, specials):


   if s == '': return s


   s_list= list (s)
   deletes = []


   l = len (s)

   literalized = s_list [0] == _SC_LITERALIZER

   try: second_letter = s_list [1]
   except IndexError: return s

   if literalized and second_letter in initials:
      deletes.append (0)
      literalized = NO

   i = 1

   if s_list [0] == _SC_ASCII [0]:
      cc, ii = _do_ascii (s, 0, l)
      if ii != 0:
         s_list [0] = cc
         deletes.extend (range (1, ii+1))
         i = ii

   while i < l:
      c = s_list [i]
      if c in specials:
         if literalized:
            deletes.append (i-1)
         literalized = NO
      elif c == _SC_LITERALIZER:
         literalized = YES
      else:
         if c == _SC_ASCII [0]:
            if not literalized:
               cc, ii = _do_ascii (s, i, l)
               if ii != i:   # an ascii value
                  s_list [i] = cc
                  deletes.extend (range (i+1, ii+1))
                  i = ii
                  c = cc
            else:
               deletes.append (i-1)

         literalized = NO
      i += 1


   for i in reversed (deletes):
      del s_list [i]


   return ''.join (s_list)



def _restore_literalizers (s, literalizer, initials, specials):

   if s == '': return s
   s_list= list (s)
   inserts = []
   if s_list [0] in initials:
      inserts.append (0)
      i = 1
   else:
      i = 0
   l = len (s)
   while i < l:
      c = s_list [i]
      if c in specials:
         inserts.append (i)
      i += 1
   for i in reversed (inserts):
      s_list.insert (i, literalizer)

   return ''.join (s_list)




########################################################


# 1 Formating definitions for translator tables (Substitution Compiler)

# The display and save formats are defined in SE.PY



########################################################



def _definition_to_translator (s, initials, specials):

    return _process_literalizers (s, initials, specials)



def _target_definition_to_translator (t):


   return _definition_to_translator (t, _TAC_INITIALS, _TAC_SPECIALS)



def _substitute_definition_to_translator (s):

   return _definition_to_translator (s, _SUC_INITIALS, _SUC_SPECIALS)





#####################################################




_IS_NOT_DEFINITION    =  0
_IS_DEFINITION        =  1
_IS_REGEX             =  2
_IS_HARD_REGEX        =  0
_IS_SOFT_REGEX        =  4
_IS_SINGLE_BYTE       =  0
_IS_MULTI_BYTE        =  4
_IS_SUBSTITUTE_FILE   =  8


_SINGLE_BYTE          = _IS_DEFINITION | _IS_SINGLE_BYTE               #  1
_MULTI_BYTE           = _IS_DEFINITION | _IS_MULTI_BYTE                #  5
_HARD_REGEX           = _IS_DEFINITION | _IS_REGEX                     #  3
_SOFT_REGEX           = _IS_DEFINITION | _IS_REGEX   | _IS_SOFT_REGEX  #  7

_SINGLE_BYTE_TO_FILE  = _SINGLE_BYTE   | _IS_SUBSTITUTE_FILE           #  9
_MULTI_BYTE_TO_FILE   = _MULTI_BYTE    | _IS_SUBSTITUTE_FILE           # 13
_HARD_REGEX_TO_FILE   = _HARD_REGEX    | _IS_SUBSTITUTE_FILE           # 11
_SOFT_REGEX_TO_FILE   = _SOFT_REGEX    | _IS_SUBSTITUTE_FILE           # 15

_IS_RUN               = 16
_IS_COMMENT           = 32



#####################################################





def _readline (f):

   """
      SE.Substitutions_Compiler._readline ()

         Quoted definitions may contain '\n' characters. Reading line by line would
         hand the definition compiler partial definitions. This function catenates
         lines with line feeds inside definitions
   """

   line = f.readline ()
   if line == '':
      return ''
   inside = NO
   quoted = NO
   literalized = NO
   i = 0

   while i < len (line):

      c = line [i]

      if c == _SC_LITERALIZER:
         literalized = YES
         i += 1
         c = line [i]
         literalized = YES
      else:
         literalized = NO

      if not inside:
         if c == '\n':
            return line

         if not c.isspace ():
            if c == _SC_QUOTE:
               if not literalized:
                  quoted = YES
            else:
               quoted = NO
            inside = YES

      else:
         if quoted:
            if c == _SC_QUOTE:
               if not literalized:
                  try:
                     if line [i+1].isspace ():
                        inside = quoted = NO
                  except IndexError:
                     inside = quoted = NO
                  i += 1
            elif c == '\n':
               next_line = f.readline ()
               if next_line == '':
                  return line
               line += next_line
         else:
            if c == _SC_COMMENT:
               return line
            if c.isspace ():
               inside = NO
      i += 1

   return line




def _do_line (line):

   expression_indexes = []

   quoted               = \
   expect_end_of_quoted = NO

   literalized          = line [0] == _SC_LITERALIZER

   if literalized:
      i = 1
      expression_indexes.append ([0])
      inside = YES

   else:
      i = 0
      inside = NO


   l = len (line)
   while i < l:

      c = line [i]


      if not inside:
         if not c.isspace ():
            if c == _SC_QUOTE:
               expression_indexes.append ([i+1])
               quoted = YES
            else:
               expression_indexes.append ([i])
            inside= YES
      else:
         if c.isspace ():
            if expect_end_of_quoted:
               expression_indexes [-1].append (i-1)
               inside = expect_end_of_quoted = quoted = NO
            else:
               if not quoted:
                  expression_indexes [-1].append (i)
                  inside = literalized = NO
         elif c == _SC_QUOTE:
            if quoted and not literalized:
               expect_end_of_quoted = YES
         else:
            expect_end_of_quoted = NO

         literalized = c == _SC_LITERALIZER

      i += 1

   if expression_indexes and len (expression_indexes [-1]) == 1:
      if expect_end_of_quoted:
         i -= 1
      expression_indexes [-1].append (i)

   return [line [x[0]:x[1]] for x in expression_indexes]




def line_to_expressions (f):

   eof = NO
   lines = ''
   indexes = []
   inside = quoted = NO
   length_of_lines = 0

   expressions = []

   ii = i = 0

   while 1:
      line = _readline (f)
      if line == '':
         break
      expression = _do_line (line)
      if expression:
         expressions.append (expression)

   return expressions




def lines_to_expressions (f):

   expressions = []
   while 1:
      exp = line_to_expressions (f)
      if exp == []:
         break
      expressions.extend (exp)
   return expressions




class Substitutions_Compiler:


   substitutions      = None
   Translator_Class   = None
   log                = None


   def __init__ (self, substitutions, Translator_Class = Translator):

      self.substitutions = substitutions
      self.Translator_Class  = Translator_Class
      self.log = []


   def __call__ (self, Translators):

      global _dud_counter


      def do_comment (s):

         pass



      def do_run ():

         T = self.Translator_Class ()
         Translators.append (T)



      def do_file (s):

         global _dud_counter

         if s in _modes.keys ():
            Translators [-1].NULL_MODE = _modes [s]
            return YES  # go on

         path_name = s


         path, name = os.path.split (s)

         try:
            if path [-1] not in '\\/':
               path += '/'
            elif DEFINITION_PATH:
               path = DEFINITION_PATH
               name = s
         except IndexError:
            pass

         path_name = path + name

         is_file_name = YES
         if path_name.rstrip () [-1] in '/\\:':
            is_file_name = NO
         try:
            if not '//' in path_name:
               os.stat (path_name)
            else:
               raise 'Network_Path'
         except (OSError, 'Network_Path'):
            is_file_name = NO

         if not is_file_name:
            self.log.append ('%s - Compiler - Ignoring single word \'%s\'. Not an existing file \'%s\'.' % (time.ctime (), s, path_name))
            _dud_counter += 1

            if _dud_counter > _DUD_LIMITER:
               response = ' '
               while response [0].lower () not in 'yn':
                  response = raw_input ('File mixup? Continue? (y/n) > ')
                  if response [0] in 'nN':
                     return NO
               _dud_counter = 0
            return YES

         f = file (path_name, 'ra')
         SC = Substitutions_Compiler (f, self.Translator_Class)
         SC (Translators)
         self.log.extend (SC.log)
         f.close ()
         return YES



      def do_definition (target, substitute):

         return Translators [-1].add_definition (target, substitute)


      _dud_counter = 0


      expressions_list = lines_to_expressions (self.substitutions)


      expression_count = 0
      number_of_expressions = reduce (lambda a, b: a + b, [len (x) for x in expressions_list], 0)

      for expressions in expressions_list:


         i = 0
         l = len (expressions)
         while i < l:

            expression = expressions [i]
            expression_count += 1

            c = expression [0]

            if c == _SC_COMMENT:
               _do_comment (expressions [i+1:])
               break

            elif expression == _SC_RUN and 1 < expression_count < number_of_expressions:
               do_run ()

            else:

               is_regex = NO
               if c == _SC_REGEX:
                  target_substitute = _do_regex (expression)
                  if target_substitute != None:
                     is_regex = YES
               if not is_regex:
                  target_substitute = _do_fixed (expression)
      
               if target_substitute == None:    # No separator
                  go_on = do_file (expression)  # Try file with dud count and exit prompt

                  if not go_on:
                     return NOT_OK
               else:
                  target, substitute = target_substitute
                  ok = do_definition (target, substitute)
                  if not ok:
                     self.log.append ('%s - Compiler - Ignoring invalid definition: %s=%s' % (time.ctime (), target, substitute))
            i += 1

      return OK



def _do_fixed (expression):

   fixed = _is_fixed.match (expression)
   if fixed:
      target = fixed.group ()
      return target [:-1], expression [len (target):]
   else:
      return None



def _do_regex (expression):

   regex = _is_regex.match (expression)
   if regex:
      target = regex.group ()
      return target [:-1], expression [len (target):]
   else:
      return None


def _do_comment (expressions):

   pass  # Not implemented






#####################################################




def _do_ascii (line, cursor, length):

   '''Converts ascii notation to character'''


   line_split = line [cursor+1:].split (_SC_ASCII [1], 1)

   if len (line_split) > 1:

      could_be_ascii = line_split [0]

      is_ascii = NO
      if could_be_ascii:
         next_c = could_be_ascii [0]
         if next_c:
            if could_be_ascii [0] in 'Xx':
               try: ascii = int (could_be_ascii [1:], 16)
               except ValueError: pass
               else: is_ascii = YES
            else:
              try: ascii = int (could_be_ascii)
              except ValueError: pass
              else: is_ascii = YES

      if is_ascii:
         if 0 <= ascii <=  255:
            return chr (ascii), cursor + len (could_be_ascii) + 1

   return line [cursor], cursor




def _comparison_function (a, b):
   if a > b [0]: return  1
   if a < b [0]: return -1
   return 0



def _binary_search (item, list, _comparison_function):

   if item == None or list == None:
      return (None, None)

   l = len (list)
   if l == 0:
      return (0, 0)

   bottom = 0
   top = l -1

   lock_index = 0    # index of topmost smaller or matching list item
   span       = 0    # No match: 0, one match: 1, multiple matches: n downward

   while 1:

      middle = (bottom + top) / 2

      m = _comparison_function (item, list [middle])

      if m == 0:

         lock_index = middle + 1
         while lock_index <= top:
            if _comparison_function (item, list [lock_index]) != 0:
               break
            lock_index += 1
         lock_index -= 1
         middle -= 1
         while middle >= 0:
            if _comparison_function (item, list [middle]) != 0:
               break
            middle -= 1
         return lock_index, lock_index - middle

      if 0 <= top - bottom <= 1:

         top_compare = _comparison_function (item, list [top])
         if top_compare > 0:
            return top + 1, 0
         if top_compare == 0:
            return top, 1
         if m < 1:
            return middle, 0
         else:
            return middle + 1, 0

      else:
         if m < 0:    # item is too small
            top = middle
         else:
            bottom = middle



_time_code_discriminator = 0


_month_numbers = \
{
   "jan" :  1,  "feb" :  2,  "mar" :  3,
   "apr" :  4,  "may" :  5,  "jun" :  6,
   "jul" :  7,  "aug" :  8,  "sep" :  9,
   "oct" : 10,  "nov" : 11,  "dec" : 12,
}

def _numerize_month (m): return _month_numbers [m[:3].lower ()]


def _number_to_letter (n):

   n = int (n)
   if n < 10: return str (n)
   return chr (n - 10 + 65)


def _time_code (t = None):

   global _time_code_discriminator

   if t == None:
      t = time.ctime ()

   s = t.split ()    # Sat May 11 08:57:33 2002

   if s [3] == '00:00:00':
      s [3] = time.ctime ().split () [3]

   cent = int (s [4]) / 100
   year = s [4][2:]
   month = _numerize_month (s [1])
   day = int (s[2])
   s = s[3].split (':')
   hour = int (s[0])
   min_code = s[1]
   sec_code = s[2]

   cent_code = chr (cent - 10 + 65)

   year_code = year

   month_code = _number_to_letter (month)
   day_code = _number_to_letter (day)
   hour_code = _number_to_letter (hour)

   _time_code_discriminator += 1

   if _time_code_discriminator == 10:
      _time_code_discriminator = 0

   time.sleep (0.1)

   return cent_code + year_code + month_code + day_code + hour_code + min_code + sec_code + str (_time_code_discriminator)




####################################################
#
#
# 6/25/2006 4:18PM  (c) 2006 Frederic Rentsch
#
#
#####################################################


