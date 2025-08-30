<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.1" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/">
  <xsl:output method="html" doctype-system="about:legacy-compat" version="1.0" encoding="UTF-8"
    indent="yes" />
  <xsl:template match="/">
    <html xmlns="http://www.w3.org/1999/xhtml" lang="en_US" xml:lang="en_US">
      <head>
        <title>
          <xsl:value-of select="/opml/head/title" />
        </title>
      </head>
      <link rel="stylesheet" href="css/style.css" />
      <link rel="stylesheet" href="css/blogroll.css" />
      <body>
        <header>
          <h1>
            <xsl:value-of select="/opml/head/title" />
          </h1>
        </header>
        <main>

          <div class="intro">
            <p>
              These are my current RSS subscriptions, for your browsing pleasure.
            </p>

            <p> If you want to import all these feeds into your feed reader, you have two options: <ol>
                <li> To download the <a href="https://en.wikipedia.org/wiki/OPML">OPML</a> version
              from a browser, click <a href="feeds.opml.xml"
                    download="feeds.opml.xml"> here.</a> Any RSS client worth its salt will let you
              import that file to automatically add all the feeds below. </li>
                <li>Alternatively, if your feed aggregator supports links to dynamic subscription
              lists, you can add the link to this page there. </li>
              </ol>
            </p>
          </div>

          <hr />

          <table>
            <xsl:for-each select="/opml/body/outline/outline">
              <tr>
                <td class="cell-feed-html-link">
                  <xsl:element name="a">
                    <xsl:attribute name="href">
                      <xsl:value-of select="@htmlUrl" />
                    </xsl:attribute>
                    <span>
                      <xsl:value-of select="@displayLink" />
                    </span>
                  </xsl:element>
                </td>
                <td class="cell-feed-rss-link">
                  <xsl:element name="a">
                    <xsl:attribute name="href">
                      <xsl:value-of select="@xmlUrl" />
                    </xsl:attribute>
                    <span>
                      [rss]
                    </span>
                  </xsl:element>
                </td>

              </tr>

            </xsl:for-each>

          </table>
          <hr />


        </main>

      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
