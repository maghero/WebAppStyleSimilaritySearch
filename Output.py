from ImgDescriptor import ImgDescriptor
import os

class Output:

    COLUMNS = 5;

    def toHTML(ids, baseURI, outputFile, image, classes, time):
        #List<ImgDescriptor> ids, String baseURI, File outputFile
        html = "<html>\n<style>\n"

        html += "</style>\n<body><h1><a href=\"/\">Home Page</a></h1>\n"

        html += "<div style=\"display:inline-block;margin-left: 15%;max-width: 300px;padding: 3px;border: 2px ridge;\">" +\
                        "<h2>Paint analyzed</h2>" +\
                        "<img src=\"" + image + "\" align=\"left\" style=\"display: block;margin-left: auto;margin-right: auto;\"><br>"

        html += "<p>Style:</p><ul>"

        for key in classes.keys():
            html += '<li>' + key + ' : ' + str("{:.2f}".format(classes[key]*100))
            html += '</li>'

        html += "</ul>"

        html += "</div>"

        html += "<h3>Search results: [time: " + time + " ms]</h3><table align='center'>\n"
        for i in range(len(ids)):
            #COLUMNS
            if i % 4 == 0:
                if i != 0:
                    html += "</tr>\n"
                html += "<tr>\n"

            html += "<td><img align='center' border='0' height='160' title='" + ids[i].getId() + ", dist: "\
                + str(ids[i].getDist()) + "' src='" + baseURI + ids[i].getId() + "'></td>\n"

        if len(ids) != 0:
            html += "</tr>\n"

        html += "</table>\n</body>\n</html>"

        if os.path.exists(outputFile):
            os.remove(outputFile)
        with open(outputFile, 'w') as output:
            output.write(html)
            print("html generated")
