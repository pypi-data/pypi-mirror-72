# -*- encoding: utf-8 -*-
# Black Hole Solver cffi-based Wrapper v0.2.3
# lib
# Copyright © 2020, Shlomi Fish.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions, and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions, and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the author of this software nor the names of
#    contributors to this software may be used to endorse or promote
#    products derived from this software without specific prior written
#    consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
lib

:Copyright: © 2020, Shlomi Fish.
:License: BSD (see /LICENSE).
"""

__title__ = 'Black Hole Solver cffi-based Wrapper'
__version__ = '0.2.3'
__author__ = 'Shlomi Fish'
__license__ = '3-clause BSD'
__docformat__ = 'restructuredtext en'

__all__ = ()

# import gettext
# G = gettext.translation('black_hole_solver', '/usr/share/locale', fallback='C')
# _ = G.gettext
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 Shlomi Fish <shlomif@cpan.org>
#
# Distributed under the terms of the Expat license.

import platform

from cffi import FFI


class BlackHoleSolverMove(object):
    """Represents a single solution move"""
    def __init__(self, column_idx):
        self._col_idx = column_idx

    def get_column_idx(self):
        """
        Returns the index of the column to move a card from.
        If it is equal num_columns, it is the talon. Else
        it is between 0 and num_columns-1.
        """
        return self._col_idx


class BlackHoleSolver(object):
    """
    The main solver class.
    """
    BLACK_HOLE_SOLVER__SUCCESS = 0
    BLACK_HOLE_SOLVER__END = 9
    BLACK_HOLE_SOLVER__OUT_OF_ITERS = 10
    # TEST:$num_befs_weights=5;
    BHS__BLACK_HOLE__BITS_PER_COL = 2
    BHS__BLACK_HOLE__MAX_NUM_CARDS_IN_COL = 3
    BHS__BLACK_HOLE__NUM_COLUMNS = 17

    def __init__(self, ffi=None, lib=None):
        self.user = None
        if ffi:
            self.ffi = ffi
            self.lib = lib
        else:
            self.ffi = FFI()
            self.lib = self.ffi.dlopen(
                "libblack_hole_solver." + (
                    "dll" if (platform.system() == 'Windows') else "so.1"))
            if not self.lib:
                self.ffi = None
                raise ImportError("Could not find shared library")
            self.ffi.cdef('''
typedef struct
{
    unsigned long nothing;
} black_hole_solver_instance_t;
int black_hole_solver_create(
black_hole_solver_instance_t **ret_instance);


int black_hole_solver_read_board(
black_hole_solver_instance_t *instance, const char *board_string,
int *error_line_number, unsigned int num_columns,
unsigned int max_num_cards_in_col, unsigned int bits_per_column);

int black_hole_solver_set_max_iters_limit(
black_hole_solver_instance_t *instance, unsigned long limit);

int black_hole_solver_enable_place_queens_on_kings(
black_hole_solver_instance_t *instance, bool enabled_status);

int black_hole_solver_enable_wrap_ranks(
black_hole_solver_instance_t *instance, bool enabled_status);

int black_hole_solver_enable_rank_reachability_prune(
black_hole_solver_instance_t *instance, bool enabled_status);

#define BLACK_HOLE_SOLVER__API__REQUIRES_SETUP_CALL 1
int black_hole_solver_config_setup(
black_hole_solver_instance_t *instance);
int black_hole_solver_setup(
black_hole_solver_instance_t *instance);

int black_hole_solver_run(
black_hole_solver_instance_t *instance);

int black_hole_solver_recycle(
black_hole_solver_instance_t *instance);

int black_hole_solver_free(
black_hole_solver_instance_t *instance);

void black_hole_solver_init_solution_moves(
black_hole_solver_instance_t *instance);
int black_hole_solver_get_next_move(
black_hole_solver_instance_t *instance, int *col_idx_ptr,
int *card_rank_ptr, int *card_suit_ptr /* Will return H=0, C=1, D=2, S=3 */
);

unsigned long black_hole_solver_get_num_states_in_collection(
black_hole_solver_instance_t *instance);

unsigned long black_hole_solver_get_iterations_num(
black_hole_solver_instance_t *instance);

int black_hole_solver_get_current_solution_board(
black_hole_solver_instance_t *instance, char *output);

const char *black_hole_solver_get_lib_version(void);
''')
        self._user_container = self.ffi.new('black_hole_solver_instance_t * *')
        self._error_on_line = self.ffi.new('int *')
        self._col_idx_ptr = self.ffi.new('int *')
        self._card_rank_ptr = self.ffi.new('int *')
        self._card_suit_ptr = self.ffi.new('int *')
        assert 0 == self.lib.black_hole_solver_create(self._user_container)
        self.user = self._user_container[0]
        self.lib.black_hole_solver_enable_rank_reachability_prune(
            self.user, 1)

    def new_bhs_user_handle(self):
        return self.__class__(ffi=self.ffi, lib=self.lib)

    def ret_code_is_suspend(self, ret_code):
        """docstring for ret_code_is_suspend"""
        return ret_code == self.BLACK_HOLE_SOLVER__OUT_OF_ITERS

    def get_next_move(self):
        """
        Returns the next move or None if they were all retrieved.
        """
        if len(self._moves):
            return self._moves.pop(0)
        return None

    def input_cmd_line(self, cmd_line_args):
        return {'last_arg': 0,
                'cmd_line_args_len': len(cmd_line_args)}

    def __del__(self):
        if self.user:
            self.lib.black_hole_solver_free(self.user)
            self.user = None
            self._user_container = None
            self._error_on_line = None
            self._col_idx_ptr = None
            self._card_rank_ptr = None
            self._card_suit_ptr = None

    NUM_COLUMNS = {'black_hole': 17, 'all_in_a_row': 13, 'golf': 7}
    MAX_NUM_CARDS_IN_COL = {'black_hole': 3, 'all_in_a_row': 4, 'golf': 5}
    BITS_PER_COL = {'black_hole': 2, 'all_in_a_row': 3, 'golf': 3}

    def read_board(self, board, game_type, place_queens_on_kings, wrap_ranks):
        """
        game_type is either 'golf' , 'black_hole' or 'all_in_a_row'
        """
        self.lib.black_hole_solver_enable_wrap_ranks(self.user, wrap_ranks)
        self.lib.black_hole_solver_enable_place_queens_on_kings(
            self.user, place_queens_on_kings)
        self.lib.black_hole_solver_config_setup(self.user)
        ret = self.lib.black_hole_solver_read_board(
            self.user,
            bytes(board, 'UTF-8'),
            self._error_on_line,
            self.NUM_COLUMNS[game_type],
            self.MAX_NUM_CARDS_IN_COL[game_type],
            self.BITS_PER_COL[game_type],
        )
        assert ret == 0
        assert 0 == self.lib.black_hole_solver_setup(self.user)
        return ret

    def resume_solution(self):
        ret = self.lib.black_hole_solver_run(self.user)
        if ret == self.BLACK_HOLE_SOLVER__SUCCESS:
            self.lib.black_hole_solver_init_solution_moves(self.user)

            def wrap():
                return self.lib.black_hole_solver_get_next_move(
                    self.user,
                    self._col_idx_ptr,
                    self._card_rank_ptr,
                    self._card_suit_ptr,
                )

            _moves = []
            ret_code = wrap()
            while ret_code == self.BLACK_HOLE_SOLVER__SUCCESS:
                _moves.append(
                    BlackHoleSolverMove(
                        column_idx=self._col_idx_ptr[0]
                    )
                )
                ret_code = wrap()
            assert ret_code == self.BLACK_HOLE_SOLVER__END
            self._moves = _moves
        return ret

    def limit_iterations(self, max_iters):
        self.lib.black_hole_solver_set_max_iters_limit(
            self.user,
            max_iters
        )

    def get_num_times(self):
        return self.lib.black_hole_solver_get_iterations_num(
            self.user)

    def get_num_states_in_collection(self):
        return self.lib.black_hole_solver_get_num_states_in_collection(
            self.user)

    def recycle(self):
        return self.lib.black_hole_solver_recycle(self.user)
