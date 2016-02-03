<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
  <body>
  <h2>Paths of Asset - <xsl:value-of select="$IPAddress" /></h2>
  <table>
    <tr>
      <th style="text-align:left">Attack Paths</th>
    </tr>
	
    <xsl:for-each select="VCReport/NmapAnalysis[@sourceNode = $IPAddress or @destinationNode = $IPAddress]">
	<tr><td><b>Performance Index: <xsl:value-of select="Path/@performanceIndex" /> - Cyber Cost: <xsl:value-of select="Path/@cyberCost" /> - Security Index: <xsl:value-of select="Path/@securityIndex" /> </b></td></tr>
    <tr><td>
	<xsl:for-each select="Path/Node">
	  <xsl:value-of select="@IPAddress" />  -> 
	  </xsl:for-each>
	  Attack </td>
    </tr>
	<tr><td><br/></td></tr>
    </xsl:for-each>
  </table>
  </body>
  </html>
</xsl:template>

</xsl:stylesheet>