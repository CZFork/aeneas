#!/usr/bin/env python
# coding=utf-8

# aeneas is a Python/C library and a set of tools
# to automagically synchronize audio and text (aka forced alignment)
#
# Copyright (C) 2012-2013, Alberto Pettarin (www.albertopettarin.it)
# Copyright (C) 2013-2015, ReadBeyond Srl   (www.readbeyond.it)
# Copyright (C) 2015-2016, Alberto Pettarin (www.albertopettarin.it)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import unittest

from aeneas.tools.execute_task import ExecuteTaskCLI
import aeneas.globalfunctions as gf


class TestExecuteTaskCLI(unittest.TestCase):

    def execute(self, parameters, expected_exit_code):
        output_path = gf.tmp_directory()
        params = ["placeholder"]
        for p_type, p_value in parameters:
            if p_type == "in":
                params.append(gf.absolute_path(p_value, __file__))
            elif p_type == "out":
                params.append(os.path.join(output_path, p_value))
            else:
                params.append(p_value)
        exit_code = ExecuteTaskCLI(use_sys=False).run(arguments=params)
        gf.delete_directory(output_path)
        self.assertEqual(exit_code, expected_exit_code)

    def test_exec_json(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/plain.txt"),
            ("", "task_language=eng|is_text_type=plain|os_task_file_format=json"),
            ("out", "sonnet.json")
        ], 0)

    def test_exec_smil(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/page.xhtml"),
            ("", "task_language=eng|is_text_type=unparsed|is_text_unparsed_id_regex=f[0-9]+|is_text_unparsed_id_sort=numeric|os_task_file_format=smil|os_task_file_smil_audio_ref=p001.mp3|os_task_file_smil_page_ref=p001.xhtml"),
            ("out", "sonnet.smil")
        ], 0)

    def test_exec_srt(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=srt"),
            ("out", "sonnet.srt")
        ], 0)

    def test_exec_srt_html(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=srt"),
            ("out", "sonnet.srt"),
            ("", "--output-html")
        ], 0)

    def test_exec_srt_skip_validator(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=srt"),
            ("out", "sonnet.srt"),
            ("", "--skip-validator")
        ], 0)

    def test_exec_srt_allow_unlisted_language(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=en-zz|is_text_type=subtitles|os_task_file_format=srt"),
            ("out", "sonnet.srt"),
            ("", "--skip-validator"),
            ("", "-r=\"allow_unlisted_languages=True\"")
        ], 0)

    def test_exec_srt_pure(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=srt"),
            ("out", "sonnet.srt"),
            ("", "-r=\"c_extensions=False\"")
        ], 0)

    def test_exec_srt_no_cdtw(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=srt"),
            ("out", "sonnet.srt"),
            ("", "-r=\"cdtw=False\"")
        ], 0)

    def test_exec_srt_no_cew(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=srt"),
            ("out", "sonnet.srt"),
            ("", "-r=\"cew=False\"")
        ], 0)

    def test_exec_srt_no_cfw(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=srt"),
            ("out", "sonnet.srt"),
            ("", "-r=\"cfw=False\"")
        ], 0)

    def test_exec_srt_no_cmfcc(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=srt"),
            ("out", "sonnet.srt"),
            ("", "-r=\"cmfcc=False\"")
        ], 0)

    def test_exec_srt_cew_subprocess(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=srt"),
            ("out", "sonnet.srt"),
            ("", "-r=\"cew_subprocess_enabled=True\"")
        ], 0)

    def test_exec_srt_head(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=srt|is_audio_file_head_length=5.000"),
            ("out", "sonnet.srt")
        ], 0)

    def test_exec_srt_tail(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=srt|is_audio_file_tail_length=5.000"),
            ("out", "sonnet.srt")
        ], 0)

    def test_exec_srt_process(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=srt|is_audio_file_process_length=40.000"),
            ("out", "sonnet.srt")
        ], 0)

    def test_exec_srt_head_process(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=srt|is_audio_file_process_length=40.000|is_audio_file_head_length=5.000"),
            ("out", "sonnet.srt")
        ], 0)

    def test_exec_srt_detect_head(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=srt|is_audio_file_detect_head_min=0|is_audio_file_detect_head_max=10.000"),
            ("out", "sonnet.srt")
        ], 0)

    def test_exec_srt_detect_tail(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=srt|is_audio_file_detect_tail_min=0|is_audio_file_detect_tail_max=10.000"),
            ("out", "sonnet.srt")
        ], 0)

    def test_exec_srt_detect_head_tail(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=srt|is_audio_file_detect_head_min=0|is_audio_file_detect_head_max=10.000|is_audio_file_detect_tail_min=0|is_audio_file_detect_tail_max=10.000"),
            ("out", "sonnet.srt")
        ], 0)

    def test_exec_srt_aba_aftercurrent(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=srt|task_adjust_boundary_algorithm=aftercurrent|task_adjust_boundary_aftercurrent_value=0.200"),
            ("out", "sonnet.srt")
        ], 0)

    def test_exec_srt_aba_beforenext(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=srt|task_adjust_boundary_algorithm=beforenext|task_adjust_boundary_beforenext_value=0.200"),
            ("out", "sonnet.srt")
        ], 0)

    def test_exec_srt_aba_offset(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=srt|task_adjust_boundary_algorithm=offset|task_adjust_boundary_offset_value=0.200"),
            ("out", "sonnet.srt")
        ], 0)

    def test_exec_srt_aba_percent(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=srt|task_adjust_boundary_algorithm=percent|task_adjust_boundary_percent_value=50"),
            ("out", "sonnet.srt")
        ], 0)

    def test_exec_srt_aba_rate(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=srt|task_adjust_boundary_algorithm=rate|task_adjust_boundary_rate_value=21.0"),
            ("out", "sonnet.srt")
        ], 0)

    def test_exec_srt_aba_rateaggressive(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=srt|task_adjust_boundary_algorithm=rateaggressive|task_adjust_boundary_rate_value=21.0"),
            ("out", "sonnet.srt")
        ], 0)

    def test_exec_srt_ignore_regex(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=srt|is_text_file_ignore_regex=\\[.*?\\]"),
            ("out", "sonnet.srt")
        ], 0)

    def test_exec_json_id_regex(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=json|os_task_file_id_regex=Word%03d"),
            ("out", "sonnet.json")
        ], 0)

    def test_exec_srt_transmap(self):
        path = gf.absolute_path("res/transliteration/transliteration.map", __file__)
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=srt|is_text_file_transliterate_map=%s" % path),
            ("out", "sonnet.srt")
        ], 0)

    def test_exec_srt_dtw_margin(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=srt"),
            ("out", "sonnet.srt"),
            ("", "-r=\"dtw_margin=30\"")
        ], 0)

    def test_exec_srt_dtw_algorithm(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=srt"),
            ("out", "sonnet.srt"),
            ("", "-r=\"c_extensions=False|dtw_algorithm=exact\"")
        ], 0)

    def test_exec_srt_mfcc_window_shift(self):
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=srt"),
            ("out", "sonnet.srt"),
            ("", "-r=\"mfcc_window_length=0.250|mfcc_window_shift=0.100\"")
        ], 0)

    def test_exec_srt_path(self):
        home = os.path.expanduser("~")
        tts_path = os.path.join(home, ".bin/myespeak")
        ffmpeg_path = os.path.join(home, ".bin/myffmpeg")
        ffprobe_path = os.path.join(home, ".bin/myffprobe")
        if gf.file_exists(tts_path) and gf.file_exists(ffmpeg_path) and gf.file_exists(ffprobe_path):
            self.execute([
                ("in", "../tools/res/audio.mp3"),
                ("in", "../tools/res/subtitles.txt"),
                ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=srt"),
                ("out", "sonnet.srt"),
                ("", "-r=\"tts_path=%s|ffmpeg_path=%s|ffprobe_path=%s\"" % (tts_path, ffmpeg_path, ffprobe_path))
            ], 0)

    def test_exec_srt_tmp_path(self):
        tmp_path = gf.tmp_directory()
        self.execute([
            ("in", "../tools/res/audio.mp3"),
            ("in", "../tools/res/subtitles.txt"),
            ("", "task_language=eng|is_text_type=subtitles|os_task_file_format=srt"),
            ("out", "sonnet.srt"),
            ("", "-r=\"tmp_path=%s\"" % (tmp_path))
        ], 0)
        gf.delete_directory(tmp_path)

    # NOTE disabling these ones as they require a network connection
    def zzz_test_exec_youtube(self):
        self.execute([
            ("", "https://www.youtube.com/watch?v=rU4a7AA8wM0"),
            ("in", "../tools/res/plain.txt"),
            ("", "task_language=eng|is_text_type=plain|os_task_file_format=txt"),
            ("out", "sonnet.txt"),
            ("", "-y")
        ], 0)

    def zzz_test_exec_youtube_largest_audio(self):
        self.execute([
            ("", "https://www.youtube.com/watch?v=rU4a7AA8wM0"),
            ("in", "../tools/res/plain.txt"),
            ("", "task_language=eng|is_text_type=plain|os_task_file_format=txt"),
            ("out", "sonnet.txt"),
            ("", "-y"),
            ("", "--largest-audio")
        ], 0)


if __name__ == "__main__":
    unittest.main()
