# Copyright (c) 2011-2016 Alexander Poluektov (alexander.poluektov@gmail.com)
#
# Use, modification and distribution are subject to the MIT license
# (See accompanying file MIT-LICENSE)

import life
import life.figures
import view

def main():
    b = life.figures.complex()
    s = life.Style()
    v = view.View(b, s, 640, 480, 3)
    v.run(200)


if __name__ == '__main__':
    main()
