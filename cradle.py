#!/usr/bin/env python
#-*- coding: windows-1251 -*-
##########################################################

from __future__ import print_function
import string
import sys

##########################################################

TAB = "\t"
Look = ""  #lookahea character

##########################################################
# Pascal specific

def WriteLn(*args):
    print(*args, sep = "")

def Write(*args):
    print(*args, sep = "", end = "")

def Read(v = None):
    global Look

    Look = sys.stdin.read(1)
    return Look

def Halt():
    print("Calling HALT")
    sys.exit(0)

def UpCase(s):
    return s.upper()

##########################################################

def GetChar():
    """Read new character from input stream"""
    return Read()

def Error(s):
    """Report an Error"""
    WriteLn()
    WriteLn("^G", "Error: ", s, ".")

def Abort(s):
    """Report and halt"""
    Error(s)
    Halt()

def Expected(s):
    """Report what was Expected"""
    Abort(s + "Expected")

def Match(x):
    """Match a specific input character"""
    if Look == x:
        GetChar()
    else:
        Expected("'" + x + "'")

##########################################################
# Boolean operators

def IsAlpha(c):
    "Recognize an alphabetic character"
    return c.upper() in string.uppercase

def IsDigit(c):
    """Recognize a decimal digit"""
    return c in string.digits

def IsAddop(c):
    return c in ["+", "-"]

##########################################################

def GetName():
    """Get an identifier"""
    if not IsAlpha(Look):
        Expected("Name")

    GetName = UpCase(Look)
    GetChar()

def GetNum():
    """Get a number"""
    if not IsDigit(Look):
        Expected("Integer")

    old_look = Look
    GetChar()
    return old_look

def Emit(s):
    """Output a string with tab"""
    Write(TAB, s)

def EmitLn(s):
    """Output a string with tab and CRLF"""
    Emit(s)
    WriteLn()

def Init():
    GetChar()

##########################################################
# Terms, Expression, etc

def Term():
    """Parse and translate a math term
       <term> ::= <factor> [<multop> <factor>]*
    """

    Factor()
    while Look in ["*", "/"]:
        EmitLn("MOVE D0,-(SP)")
        if Look == "*":
            Multiply()
        elif Look == "/":
            Divide()
        else:
            Expected("Multop")

def Factor():
    """Parse and translate a math factor
       <factor> ::= (expression)
    """
    if Look == "(":
        Match("(")
        Expression()
        Match(")")
    elif IsAlpha(Look):
        EmitLn("MOVE " + GetName() + "(PC),DO")
    else:
        EmitLn("MOVE #" + GetNum() + ",D0")

def Expression():
    """<expression> ::= <term> [<addop> <term>]* """

    if IsAddop(Look):  # if input '-3' transfer to "0 - 3"
        EmitLn("CLR D0")
    else:
        Term()

    while IsAddop(Look):
        EmitLn("MOVE D0, -(SP)") # push to stack
        if Look == "+":
            Add()
        elif Look == "-":
            Subtract()
        else:
            Expected("Addop")

######################
# Arithmetic operators

def Add():
    Match("+")
    Term()
    EmitLn("ADD (SP)+, D0")

def Subtract():
    Match("-")
    Term()
    EmitLn("SUB (SP)+, D0")
    EmitLn("NEG D0")

def Multiply():
    Match("*")
    Factor()
    EmitLn("MULS (SP)+,D0")

def Divide():
    Match("/")
    Factor()
    EmitLn("MOVE (SP)+,D1")
    EmitLn("DIVS D1,D0")

##########################################################

def mainPascalProcedure():
    Init()
    # print("after Init()")
    Expression()
    # Term()

##########################################################

if __name__ == "__main__":
    mainPascalProcedure()

##########################################################
# EOF