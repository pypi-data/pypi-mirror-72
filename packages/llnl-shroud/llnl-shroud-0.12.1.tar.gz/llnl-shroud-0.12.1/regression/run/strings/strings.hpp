// Copyright (c) 2017-2020, Lawrence Livermore National Security, LLC and
// other Shroud Project Developers.
// See the top-level COPYRIGHT file for details.
//
// SPDX-License-Identifier: (BSD-3-Clause)
// #######################################################################
//
// strings.hpp - wrapped routines
//

#ifndef STRINGS_HPP
#define STRINGS_HPP

#include <string>

void passChar(char status);
void passCharForce(char status);
char returnChar();

void passCharPtr(char * dest, const char *src);
void passCharPtrInOut(char * s);

const char * getCharPtr1();
const char * getCharPtr2();
const char * getCharPtr3();
const char * getCharPtr4();

const std::string getConstStringResult();
const std::string getConstStringLen();
const std::string getConstStringAsArg();
const std::string getConstStringAlloc();

const std::string& getConstStringRefPure();
const std::string& getConstStringRefLen();
const std::string& getConstStringRefAsArg();
const std::string& getConstStringRefLenEmpty();
const std::string& getConstStringRefAlloc();

const std::string * getConstStringPtrLen();
const std::string * getConstStringPtrAlloc();
const std::string * getConstStringPtrOwnsAlloc();
const std::string * getConstStringPtrOwnsAllocPattern();

void acceptName_instance(std::string arg1);

void acceptStringConstReference(const std::string & arg1);

void acceptStringReferenceOut(std::string & arg1);

void acceptStringReference(std::string & arg1);

void acceptStringPointerConst(const std::string * arg1);

void acceptStringPointer(std::string * arg1);

void fetchStringPointer(std::string * arg1);

void acceptStringPointerLen(std::string * arg1, int *len);

void fetchStringPointerLen(std::string * arg1, int *len);

void returnStrings(std::string & arg1, std::string & arg2);

char returnMany(int * arg1);

void explicit1(char * name);
void explicit2(char * name);

extern "C" {
  void CpassChar(char status);
  char CreturnChar();

  void CpassCharPtr(char * dest, const char *src);
}

void PostDeclare(int *count, std::string &name);


#endif // STRINGS_HPP
