from ImgDescriptor import ImgDescriptor
import os

class Output:

    COLUMNS = 5;

    def toHTML(ids, baseURI, outputFile, image, styleClasses, artistClasses, time):
        #List<ImgDescriptor> ids, String baseURI, File outputFile
        html = "<html><head><title>Similarity Paintings</title><link rel=\"stylesheet\" href=\"https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css\" integrity=\"sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z\" crossorigin=\"anonymous\">\n<style>\n a { text-decoration: inherit; color: inherit;}\n"

        html += "</style>\n</head>\n<body style=\"text-align: center; background-color:rgb(255, 255, 217);\"><h1><a href=\"/\">Similarity Paintings Search Engine</a> </h1><hr>\n"

        html += "<div style=\"display:inline-block;padding: 3px;border: 2px ridge;\">" +\
                        "<h3>Paint analyzed</h3><hr>" +\
                        "<img src=\"" + image + "\" align=\"left\" style=\"display: block;margin-left: auto;margin-right: auto;\"><br>"

        if len(list(styleClasses.keys())) == 1:
            html += "<div style=\"text-align:left\"><p>Predicted Style:</p><ul>"
        else:
            html += "<div style=\"text-align:left\"><p>Predicted Styles:</p><ul>"

        for key in styleClasses.keys():
            html += '<li>' + key + ' : ' + str("{:.2f}".format(styleClasses[key]*100)) + ' %'
            html += '</li>'

        html += "</ul>"

        if len(list(artistClasses.keys())) == 1:
            html += "<p>Predicted Artist:</p><ul>"
        else:
            html += "<p>Predicted Artists:</p><ul>"

        for key in artistClasses.keys():
            html += '<li>'
            for splittedName in key.split('_'):
                html += splittedName.lower().capitalize() + ' '
            html += ': ' + str("{:.2f}".format(artistClasses[key]*100)) + ' %'
            html += '</li>'

        html += "</ul>"

        html += "</div></div>"

        html += "<h3 style=\"text-align: left\">Search results: [time: " + time + " ms]</h3><table align='center'>\n"
        for i in range(len(ids)):
            #COLUMNS
            if i % 5 == 0:
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
