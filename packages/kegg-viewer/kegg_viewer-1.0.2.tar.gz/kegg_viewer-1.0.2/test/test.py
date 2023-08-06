#!/usr/bin/env python
# -*- coding=utf-8 -*-

from pysvg.structure import Svg, Image
from pysvg.shape import Rect, Circle
from pysvg.style import Style
from pysvg.linking import A
from pysvg.text import Text


base_url = 'https://www.genome.jp'

width, height = 1338, 880

svg = Svg(width=width, height=height)
# svg.set_xml_lang('en')

im = Image(x=0, y=0, width=width, height=height)
# im.setAttribute('xlink:href', 'hsa05416.png')
im.set_xlink_href('hsa05416.png')
svg.addElement(im)


a = A(target='new_window')
a.set_xlink_title('6444 (SGCD)')
a.set_xlink_href(base_url + '/dbget-bin/www_bget?hsa:6444')

style_dict = {
    'fill-opacity': '0.5',
    'fill': 'green',
    'stroke': 'green',
    'stroke-opacity': '1',
    'stroke-width': '2'
}
style = '; '.join((':'.join(each) for each in style_dict.items()))

x, y, rx, ry, = 586, 216, 632, 233
width = rx -x
height = ry - y

rect = Rect(x=x, y=y, width=width, height=height)
rect.set_style(style)
a.addElement(rect)
svg.addElement(a)

circle = Circle(239, 617, 4)
circle.set_style('stroke: red')
svg.addElement(circle)

svg.save('out.svg', encoding ='UTF-8', standalone='no')

