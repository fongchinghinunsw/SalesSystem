/* https://script.google.com/a/adamyi.com/d/1dKY6VDytDJLUzWO9HSm8nPH6uH2BOKfzlbB0fkQLVofiCiEn6qNQ7PyN/edit */

function createDocument() {
  var dataId = '1wZ794XR8N1M9bWgASx4JkzMh-WmmB8M1dfChf0Xzh8Y';
  var templateId = '1gG6uDwuZrf-de4nMWMmc-ZlkCghr1cPl4DRn776kwCI';
  var targetId = '18cd048HCGWWj9Pxx0DIyPlCec7mcsh0LN66ZKyXKw30';
  
  var currentDate = Utilities.formatDate(new Date(), "GMT", "yyyy-MM-dd HH:mm") + " (UTC)"; 
  // var modifyDate = Utilities.formatDate(DriveApp.getFileById(dataId).getLastUpdated(), timezone, "yyyy-MM-dd HH:mm"); 
  
  var headers = Sheets.Spreadsheets.Values.get(dataId, 'user!A1:G1');
  var stories = Sheets.Spreadsheets.Values.get(dataId, 'user!A2:G10');
  
  var template = DocumentApp.openById(templateId).getBody();
  var targetBody = DocumentApp.openById(targetId).getBody();
  Logger.log(template);
  
  targetBody.appendParagraph("The following tables are auto-generated at: " + currentDate);
  targetBody.appendParagraph("NOTES: Do not modify the following tables by hand in the doc. Modify it in the spreadsheet, and ping adamyi@ to regenerate the following tables.");
  
  for (var i = 0; i < stories.values.length; i++) {
    
    var tmp = template.copy();
    
    for (var j = 0; j < headers.values[0].length; j++) {
      var header = headers.values[0][j];
      var value = stories.values[i][j];
      tmp.replaceText('##' + header + '##', value);
    }
    
    mergeBodies(targetBody, tmp);
    
  }

}

/* Snippet from http://stackoverflow.com/questions/10692669 */
function mergeBodies(body, other) {
  var totalElements = other.getNumChildren();
  for (var j = 0; j < totalElements; ++j) {
    var element = other.getChild(j).copy();
    var type = element.getType();
    if (type == DocumentApp.ElementType.PARAGRAPH)
      body.appendParagraph(element);
    else if (type == DocumentApp.ElementType.TABLE)
      body.appendTable(element);
    else if (type == DocumentApp.ElementType.LIST_ITEM)
      body.appendListItem(element);
    else
      throw new Error("According to the doc this type couldn't appear in the body: " + type);
  }
}
