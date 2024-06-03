
window.onload = function () {
  var str = "";//定义用于拼接的字符串
  for (let i = 0; i < item_list.length; i++) {
    //拼接表格的行和列
    str = "<tr><td>" + item_list[i][0] + "</td><td>" + item_list[i][1] + "</td><td>" + item_list[i][2] +"</td><td>" + item_list[i][3] + "</td><td>" + item_list[i][4] +    "</td><td>" + item_list[i][5] +   "</td><td>" + item_list[i][6] +   "</td></tr>" ;
    //追加到table中
    $("#tech-companies-1").append(str);
  }
  document.getElementById("sum").innerHTML=n;
}