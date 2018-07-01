# FORMEX.py


"""

   Formula Expander - A derivation from SE, using SE's substitution-cascading capability.

   >>> circle = FORMEX.Formula_Expander ('perimeter = d * pi, d = r + r, r = 99.9')
   >>> circle ('perimeter')
   Cannot evaluate ((99.9 + 99.9) * pi)

   >>> circle.define ('pi = 3.14')
   >>> circle ('perimeter')
   Cannot evaluate ((r + r) * (3.14))

   >>> circle.define ('area = r * r * pi')
   >>> circle.expand ('area')
   '((99.9) * (99.9) * (3.14159))'
   >>> circle ('area')
   31337.231400000008

   >>> circle.define ('pi = "math.pi"') # Redefine pi. Double-quote terminals living in the environment.  
   >>> circle.expand ('area')
   '((99.9) * (99.9) * (math.pi))'
   >>> circle ('area')
   31353.126098752677

   >>> circle.define ('cm_per_inch = 2.54, km_per_mile = 1.61')
   >>> circle.expand ('cm_per_inch * perimeter')
   '(2.54) * (((99.9) + (99.9)) * (math.pi))'
   >>> circle ('cm_per_inch * perimeter')
   1594.3331389555915

   ... etc.


"""



import SE, SEL, sys

import math



__version__   = 1.0
__author__    = SEL.__author__
__copyright__ = SEL.__copyright__




# The symbols in a formula need to be registered. This filters them out:

_Symbols_Filter = SEL.SEL ('<EAT> "~[a-zA-Z"\'][a-zA-Z0-9_"\'.]*~==(32)')
                

# show_system () gets all definitions from SE.Translator._show (). The 
# target locks are of no interest, however and are filtered out for the display. 

_Lock_Filter    = SEL.SEL (r'"~.*?==.*\n~=" \\(=( \\==\= (34)= (39)= ')




YES, NO = 1, 0

_ORDER      =  0  
_RVALUES    =  1
_LVALUE     =  2
_FORMULA    =  3


class Formula_Expander (SE.SE):
         
   steps = 0

   def __init__ (self, equations = None):
      SE.SE.__init__ (self, '')
      self.organizer = {}
      if equations:
         self.define (equations)

   def define (self, equations):
      for equation in [x.strip () for x in equations.split (',')]:
         self._define (equation)
      self._build ()

   def _define  (self, equation):
      try: lvalue, formula = [x.strip () for x in equation.split ('=', 1)] 
      except ValueError:
         sys.stderr.write ('%s is not an equation\n' % equation)
         return
      rvalues = _Symbols_Filter (formula).split ()
      formula = formula.replace ('"', '').replace ("'", "")
      self.organizer [lvalue] = [0, rvalues, lvalue, formula]  

                                                                               
   def _build (self):

      terminals  = []
      dependents = []

      for lvalue in self.organizer:
         if self.organizer [lvalue][_RVALUES] == []:
            self.organizer [lvalue][_ORDER] = 0
            terminals.append (self.organizer [lvalue])
         else:
            o = self.organizer [lvalue]
            o [_ORDER] = 1
            dependents.append (o)

      lvalues = self.organizer.keys ()
      rvalues = reduce (lambda a, b: a + b, [x [_RVALUES] for x in self.organizer.values ()])
      rvalues.sort ()
      unique (rvalues)
      number_of_non_terminals = len (rvalues)
      #? iteration_limit = number_of_non_terminals

      done = NO
      iteration_counter = 0

      while not done:
         iteration_counter += 1
         done = YES
         for dependent_1 in dependents:
            for dependent_2 in dependents:
               if dependent_1 is dependent_2:
                  if dependent_1 [_LVALUE] in dependent_2 [_RVALUES]:
                     sys.stderr.write ('Cannot resolve self-refererring equation: %s = %s\n' % (dependent_1 [_LVALUE], dependent_2 [_FORMULA]))
                     return
               else:
                  if dependent_1 [_LVALUE] in dependent_2 [_RVALUES]:
                     if dependent_1 [_ORDER] >= dependent_2 [_ORDER]:
                        dependent_2 [_ORDER] = dependent_1 [_ORDER] + 1
                        done = NO

      dependents.sort ()
      number_of_translators = dependents [-1][_ORDER] + 1

      for item in self.organizer.values ():
         item [_ORDER] = number_of_translators - item [_ORDER] - 1

      Translators = [SE.Translator () for i in range (number_of_translators)]
      current_index = 0
      
      for item in self.organizer.values ():
         Translators [item [_ORDER]].add ('"%s=\(%s)"' % (item [_LVALUE], item [_FORMULA].replace ('=', '\=')))

      # All lvalues must be locked towards the beginning
      up_locks = {}
      # Terminals which the runtime environment resolves (quoted, e.g. math.log) must be locked towards the end.
      down_locks = {}  
      for item in self.organizer.values ():
         lvalue = item [_LVALUE]
         if len (lvalue) > 1:
            up_locks [lvalue] = item [_ORDER]
         for value in item [_RVALUES]:
            if value [0] in "\x22'":
               lock_this = value [1:-1]
               if down_locks.has_key (lock_this):
                  down_locks [lock_this].append (item [_ORDER])
               else:
                  down_locks [lock_this] = [item [_ORDER]]

      for lvalue in up_locks:
         i = up_locks [lvalue]
         while i:
            i -= 1
            Translators [i].add ('"%s=="' % lvalue)
         
      for value in down_locks:
         i = min (down_locks [value]) + 1
         while i < number_of_translators:
            Translators [i].add ('"%s=="' % value)
            i += 1
      self.Translators = Translators


   # The target locks are of no interest and are filtered out by _Lock_Filter

   def _all_definitions (self):
      show = ''
      level = 1
      for T in self.Translators:
         definitions = T._all_definitions ().splitlines ()
         for definition in definitions:
            if definition.find ('==') >= 0:
               continue
            show += '   %2d  %s\n' % (level, definition)
         level += 1
      return _Lock_Filter (show)


   def show_system (self):
      all_rvalues = reduce (lambda a, b: a + b, [x [_RVALUES] for x in self.organizer.values ()])
      unique (all_rvalues)
      organizer = self.organizer
      print
      print 'All equations\n'
      print self._all_definitions ()
      print
      print 'Unresolved or external input variables\n'
      for rvalue in all_rvalues:
         if rvalue not in organizer.keys ():
            print '  ', rvalue.replace ('"', '').replace ("'", "")
      print
         


   def expand (self, lvalue): return SE.SE.__call__ (self, lvalue)


   def __call__ (self, lvalue):
      expression = SE.SE.__call__ (self, lvalue)
      try: return eval (expression)
      except NameError: sys.stderr.write ('Cannot evaluate %s\n' % expression)





##############


def unique (l):

   """
      STDUTIL.unique (list)

         Takes out all duplicates. List is expected to be sorted.
         Will unique contiguous repeats in unsorted lists.

   """

   delete_list = []

   previous_item = l [0]
   i = 1
   length = len (l)
   while i < length:
      item = l [i]
      if item == previous_item:
         delete_list.append (i)
      else:
         previous_item = item
      i += 1

   delete_list.reverse ()

   for i in delete_list:
      del l [i]
