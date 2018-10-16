suite('rb/diffviewer/models/DiffCommit', function() {
    describe('parse', function() {
        it('Short commit message', function() {
            const model = new RB.DiffCommit(
                {
                    author_name: 'Author Name',
                    commit_id: 'r123',
                    commit_message: 'A commit message.\n',
                }, {parse: true});

            expect(model).toBeTruthy();
            expect(model.attributes).not.toBe(undefined);
            expect(model.attributes).toEqual({
                authorName: 'Author Name',
                commitID: 'r123',
                commitMessage: 'A commit message.',
                summary: 'A commit message.',
            });
            expect(model.hasSummary()).toBe(false);
        });

        it('Long commit message', function() {
            const model = new RB.DiffCommit(
                {
                    author_name: 'Author Name',
                    commit_id: 'r123',
                    commit_message: dedent`
                        This is a long commit message.

                        It spans several lines.
                        It has trailing newlines as well.


                    `,
                }, {parse: true});

            expect(model).toBeTruthy();
            expect(model.attributes).not.toBe(undefined);
            expect(model.attributes).toEqual({
                authorName: 'Author Name',
                commitID: 'r123',
                commitMessage: (
                    'This is a long commit message.\n\n' +
                    'It spans several lines.\n' +
                    'It has trailing newlines as well.'
                ),
                summary: 'This is a long commit message.',
            });
            expect(model.hasSummary()).toBe(true);
        });

        it('Commit message with overlong first line', function() {
            const message = 'abcd'.repeat(100);
            const summary = message.substr(0, 77) + '...';
            const model = new RB.DiffCommit(
                {
                    author_name: 'Author Name',
                    commit_id: 'r234',
                    commit_message: message,
                },
                {parse: true});

            expect(model).toBeTruthy();
            expect(model.attributes).not.toBe(undefined);
            expect(model.attributes).toEqual({
                authorName: 'Author Name',
                commitID: 'r234',
                commitMessage: message,
                summary: summary,
            });
            expect(model.hasSummary()).toBe(true);
        });
    });
});