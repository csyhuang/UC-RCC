#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function

__source__ = "sidebyside.py"
__author__ = "Frank J. Greco"
__copyright__ = "Copyright 2015-2018, Frank J. Greco"
__credits__ = []
__license__ = "Apache"
__version__ = "1.0.1"
__maintainer__ = ""
__email__ = ""
__status__ = "Development"

def sidebyside(hm,text_list):
    from bokeh.embed import components
    script, div = components(hm)

    tl = ''
    for i in range(0, 217):
        tl = tl + '<br> {} : {}'.format(str(i),)



    d = {'script': script, 'div': div, 'text': text}

    html = """
     <!DOCTYPE html>
     <html lang="en">
         <head>

             <meta charset="utf-8">
             <title>Bokeh Scatter Plots</title>

             <link rel="stylesheet" href="http://cdn.pydata.org/bokeh/release/bokeh-0.12.6.min.css" type="text/css" />
             <script type="text/javascript" src="http://cdn.pydata.org/bokeh/release/bokeh-0.12.6.min.js"></script>

             %(script)s

         </head>
         <body>
          <table style="width:100">
           <tr>
             <th> %(div)s </th>
             <th>  
                 <div style="overflow: auto; width:300px; height:400px;">
                 %(text)s.
                 </div
             </th>

           </table> 
         </body>
     </html>
     """

    b2html = html % d

    fd = open('b3.html', 'w')
    fd.write(b2html)
