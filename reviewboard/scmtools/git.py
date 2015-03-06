import platform
    supports_authentication = True
    DIFF_GIT_LINE_RES = [
        # Match with a/ and b/ prefixes. Common case.
        re.compile(
            b'^diff --git'
            b' (?P<aq>")?a/(?P<orig_filename>[^"]+)(?(aq)")'
            b' (?P<bq>")?b/(?P<new_filename>[^"]+)(?(bq)")$'),

        # Match without a/ and b/ prefixes. Spaces are allowed only if using
        # quotes around the filename.
        re.compile(
            b'^diff --git'
            b' (?P<aq>")?(?!a/)(?P<orig_filename>(?(aq)[^"]|[^ ])+)(?(aq)")'
            b' (?P<bq>")?(?!b/)(?P<new_filename>(?(bq)[^"]|[^ ])+)(?(bq)")$'),

        # Match without a/ and b/ prefixes, without quotes, and with the
        # original and new names being identical.
        re.compile(
            b'^diff --git'
            b' (?!")(?!a/)(?P<orig_filename>[^"]+)(?!")'
            b' (?!")(?!b/)(?P<new_filename>(?P=orig_filename))(?!")$'),
    ]

        diff_git_line = self.lines[linenum]

        file_info.data = diff_git_line + b'\n'
        line = self.lines[linenum]

            file_info.data += line + b"\n"
            file_info.data += line + b"\n"
            file_info.data += line + b"\n"
            rename_from = self.lines[linenum + 1]
            rename_to = self.lines[linenum + 2]

            file_info.origFile = rename_from[len(b'rename from '):]
            file_info.newFile = rename_to[len(b'rename to '):]

            file_info.data += line + b"\n"
            file_info.data += rename_from + b"\n"
            file_info.data += rename_to + b"\n"
            copy_from = self.lines[linenum + 1]
            copy_to = self.lines[linenum + 2]

            file_info.origFile = copy_from[len(b'copy from '):]
            file_info.newFile = copy_to[len(b'copy to '):]

            file_info.data += line + b"\n"
            file_info.data += copy_from + b"\n"
            file_info.data += copy_to + b"\n"
                orig_line = self.lines[linenum]
                new_line = self.lines[linenum + 1]

                orig_filename = orig_line[len(b'--- '):]
                new_filename = new_line[len(b'+++ '):]

                if orig_filename.startswith(b'a/'):
                    orig_filename = orig_filename[2:]

                if new_filename.startswith(b'b/'):
                    new_filename = new_filename[2:]

                if orig_filename == b'/dev/null':
                    file_info.origFile = new_filename
                else:
                    file_info.origFile = orig_filename
                if new_filename == b'/dev/null':
                    file_info.newFile = orig_filename
                else:
                    file_info.newFile = new_filename

                file_info.data += orig_line + b'\n'
                file_info.data += new_line + b'\n'
        if not file_info.origFile:
            # This file didn't have any --- or +++ lines. This usually means
            # the file was deleted or moved without changes. We'll need to
            # fall back to parsing the diff --git line, which is more
            # error-prone.
            assert not file_info.newFile

            self._parse_diff_git_line(diff_git_line, file_info, linenum)

        if isinstance(file_info.origFile, six.binary_type):
            file_info.origFile = file_info.origFile.decode('utf-8')

        if isinstance(file_info.newFile, six.binary_type):
            file_info.newFile = file_info.newFile.decode('utf-8')

    def _parse_diff_git_line(self, diff_git_line, file_info, linenum):
        """Parses the "diff --git" line for filename information.

        Not all diffs have "---" and "+++" lines we can parse for the
        filenames. Git leaves these out if there aren't any changes made
        to the file.

        This function attempts to extract this information from the
        "diff --git" lines in the diff. It supports the following:

        * All filenames with quotes.
        * All filenames with a/ and b/ prefixes.
        * Filenames without quotes, prefixes, or spaces.
        * Filenames without quotes or prefixes, where the original and
          modified filenames are identical.
        """
        for regex in self.DIFF_GIT_LINE_RES:
            m = regex.match(diff_git_line)

            if m:
                file_info.origFile = m.group('orig_filename')
                file_info.newFile = m.group('new_filename')
                return

        raise DiffParserError(
            'Unable to parse the "diff --git" line for this file, due to '
            'the use of filenames with spaces or --no-prefix, --src-prefix, '
            'or --dst-prefix options.',
            linenum)

            if platform.system() == "Windows":
                # Windows requires drive letter (e.g. C:/)
                self.git_dir = url_parts[1] + url_parts[2]
            else:
                self.git_dir = url_parts[2]