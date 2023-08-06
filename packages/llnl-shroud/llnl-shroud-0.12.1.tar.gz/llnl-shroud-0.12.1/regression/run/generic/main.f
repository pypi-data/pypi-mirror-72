! Copyright (c) 2017-2020, Lawrence Livermore National Security, LLC and
! other Shroud Project Developers.
! See the top-level COPYRIGHT file for details.
!
! SPDX-License-Identifier: (BSD-3-Clause)
! #######################################################################
!
! Test Fortran API generated from generic.yaml.
!

program tester
  use fruit
  use iso_c_binding
  use generic_mod
  implicit none
  logical ok

  call init_fruit

  call test_functions
  call test_database

  call fruit_summary
  call fruit_finalize

  call is_all_successful(ok)
  if (.not. ok) then
     call exit(1)
  endif

contains

  subroutine test_functions
    integer(C_LONG) rv

    call set_case_name("test_functions")

    call generic_real(1.0)
    call assert_equals(1.0d0, get_global_double(), "generic_real real")

    call generic_real(2.0d0)
    call assert_equals(2.0d0, get_global_double(), "generic_real double")

    rv = generic_real2(1_C_INT, 2_C_INT)
    call assert_true(3_C_LONG == rv, "generic_real2 int")

    rv = generic_real2(10_C_LONG, 20_C_LONG)
    call assert_true(30_C_LONG == rv, "generic_real2 long")

  end subroutine test_functions

  subroutine test_database
    real(C_FLOAT) var1(10)
    integer(C_INT)  itype
    integer(C_SIZE_T) isize
    type(C_PTR) fwa

    call set_case_name("test_database")

    call save_pointer(var1)

    fwa = C_NULL_PTR
    call get_pointer(fwa, itype, isize)
    call assert_true(c_associated(fwa), "fwa is not none")
    call assert_true(T_FLOAT == itype, "type of var1")
    call assert_true(size(var1) == isize, "size of var1")

    call save_pointer2(var1)

    fwa = C_NULL_PTR
    call get_pointer(fwa, itype, isize)
    call assert_true(c_associated(fwa), "fwa is not none")
    call assert_true(T_FLOAT == itype, "type of var1")
    call assert_true(size(var1) == isize, "size of var1")

  end subroutine test_database

end program tester
