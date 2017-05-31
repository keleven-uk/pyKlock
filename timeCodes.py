# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 15:42:00 2015

@author: scottk2
"""

#  GLOBAL variables used in several functions

hours = ("twelve", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",  "eleven", "twelve")
units = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve")
tens = ("zero", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty")

minsText = {0: "", 5: "five past", 10: "ten past", 15: "quarter past", 20: "twenty past", 25: "twenty-five past", 30: "half past",
           35: "twenty-five to", 35: "twenty-five to", 40: "twenty to", 45: "quarter to", 50: "ten to", 55: "five to", 60: ""}


romanNumerals = { 0: ".",
                  1: "I",
                  2: "II",
                  3: "III",
                  4: "IV",
                  5: "V",
                  6: "VI",
                  7: "VII",
                  8: "VIII",
                  9: "IX",
                 10: "X",
                 11: "XI",
                 12: "XII",
                 13: "XIII",
                 14: "XIV",
                 15: "XV",
                 16: "XVI",
                 17: "XVII",
                 18: "XVIII",
                 19: "IXX",
                 20: "XX",
                 21: "XXI",
                 22: "XXII",
                 23: "XXIII",
                 24: "XXIV",
                 25: "XXV",
                 26: "XXVI",
                 27: "XXVII",
                 28: "XXVIII",
                 29: "XXIX",
                 30: "XXX",
                 31: "XXXI",
                 32: "XXXII",
                 33: "XXXIII",
                 34: "XXXIV",
                 35: "XXXV",
                 36: "XXXVI",
                 37: "XXXVII",
                 38: "XXXVIII",
                 39: "XXXIX",
                 40: "XL",
                 41: "XLI",
                 42: "XLII",
                 43: "XLIII",
                 44: "XLIV",
                 45: "XLV",
                 46: "XLVI",
                 47: "XLVII",
                 48: "XLVIII",
                 49: "IL",
                 50: "L",
                 51: "LI",
                 52: "LII",
                 53: "LIII",
                 54: "LIV",
                 55: "LV",
                 56: "LVI",
                 57: "LVII",
                 58: "LVIII",
                 59: "LVIX",
                 60: "LX"
                 }

morseCode = {0: "-----",
             1: "·----",
             2: "··---",
             3: "···--",
             4: "····-",
             5: "·····",
             6: "-····",
             7: "--···",
             8: "---··",
             9: "----·"
             }
