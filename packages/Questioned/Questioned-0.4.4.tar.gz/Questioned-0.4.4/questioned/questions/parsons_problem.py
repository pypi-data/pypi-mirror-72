"""
This module defines the manual entry question.
"""

import random
import html

from questioned.utils import select_questions

from .question import Question


class ParsonsProblem(Question):
    """
    Defines a parsons problem that is input manually using the exam_spec file.

    This question type is based on a paper by Paul Denny, Andrex Luxton-Reilly
    and Beth Simon. The paper can be found at
    https://cseweb.ucsd.edu/classes/fa08/cse599/denny.pdf

    Though the basic structure of this question type is similar to the one
    described in the paper. It does not support the more complex rubrics that
    would require a human to correct the exam.

    Instead, it is best to focus on shorter code snippets where ordering is
    the main focus of the problem.

    The parsons problem requires additional information through the ``exam_spec``.

    For example:
    ::
        parsons_problems:
        - description: "Pyramid printing function."
          code: |
            #include<stdio.h>
            int main() {
                int i, j, rows;
                printf("Enter number of rows: ");
                scanf("%d", &rows);
                for (i=1; i<=rows; ++i) {
                    for (j=1; j<=i; ++j)
                    { printf("* "); }
                    printf("\\n");}
                return 0;}

    All parsons problems require at least a description and a code segment.

    The code segment is automatically broken up into lines and jumbled for
    the assignment. As such it must be entered in the correct form.
    """

    # The dynamic use of attributes in this class causes pylint to falsely flag no-member
    # pylint: disable=no-member

    def render_blackboard(self):
        """
        Render the parsons problem for blackboard.
        Uses the JUMBLED_SENTENCE type.
        """
        # Create choice-answer pairs
        ca_tuples = []
        answer_lines = self.answer.split('\n')
        question_lines = self.question.split('\n')
        for line_nr in range(len(answer_lines)-1):
            ca_tuples.append([line_nr, answer_lines[line_nr], question_lines[line_nr]])

        if self.image is not None:
            image = self.image
        else:
            image = ""

        # In this case, this length is acceptable
        # pylint: disable=line-too-long
        out = f"JUMBLED_SENTENCE\t{image}Please reassemble the following code snippets to form a {self.description}.<br/><br/>"
        out += "<pre>"
        for line in question_lines:
            if line.strip() == '':
                continue
            escaped_line = html.escape(
                line.replace('[', '&#91;')\
                    .replace(']', '&#93;')
            )
            out += ' - '
            out += escaped_line.strip()
            out += '<br />'

        out += '</pre>'

        # Place variable fields:
        for tup in ca_tuples:
            out += f"[{tup[0]}]<br/>"

        out += '\t'

        # Add answers
        for tup in random.sample(ca_tuples, k=len(ca_tuples)):
            out += f'{tup[1]}\t{tup[0]}\t\t'

        out = out[:-2] # Remove extraneous tabs

        out += '\n'
        return out


    def render_markdown(self):
        """
        Render the parsons problem to markdown.
        """
        out = f"Please reassemble the following code snippets to form a {self.description}.\n\n"
        for line in self.question.split('\n'):
            out += f"\t {line.strip()}\n"

        return out

    @classmethod
    def generate(cls, exam_spec, count: int = 1, section_data=None):
        """
        Generates an amount of manually input questions.
        """

        # False positive
        # pylint: disable=unsubscriptable-object

        if section_data is None:
            section_data = {}

        out = []
        selection = select_questions(cls, exam_spec, 'parsons_problems', count, section_data)
        for selected_problem in selection:
            lines = selected_problem['code'].split('\n')
            jumbled_lines = random.sample(lines, k=len(lines))

            jumbled_str = "\n".join(jumbled_lines)

            problem = cls(exam_spec,
                          jumbled_str,
                          selected_problem['code'],
                          description=selected_problem['description'],
                          question_data=selected_problem
                         )
            out.append(problem)
        return out
