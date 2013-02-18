'''Gets the student names of the different programs at
Polytechnique Montreal University'''

from scraptools import getElements

def getAdmittedStudents(program, year):
    '''Returns the name of the students who joined the program in a given year'''
    href = 'http://eduportfolio.org/groupes/view/portfolio_{0}{1}{2}'\
    .format(program.lower(), year, str(year + 1)[2:])

    ret = []
    for row in getElements(href, 'td:nth-child(2)'):
        name = row.text.rstrip()
        ret.append(name)
    return ret

#Example programs
#programs = ['gch', 'civ', 'ele', 'glq', 'mtr','min', 'mec', 'phs', 'ergo', 'gbm']

#Example to get computer science students
for program in ('inf', 'log'):
    for year in xrange(2007, 2013):
        print program, year
        students = getAdmittedStudents(program, year)
        print '\n'.join(students)
        print