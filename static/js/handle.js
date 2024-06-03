var item_list = [];
for(var i=0;i<n;i++){
    var temp_list = [];
    temp_list.push(date_list[i]);
    if(physical_list[i]==1){
        temp_list.push('涨');
    }
    else{
        temp_list.push('跌');
    }
    if(forecast_result_list[i]==1){
        temp_list.push('涨');
    }
    else if(forecast_result_list[i]==0){
        temp_list.push('跌');
    }
    else{
        temp_list.push('预测准确度低');
    }
    temp_list.push(accuracy_list[i]);
    temp_list.push(result_sum_list[i]);
    temp_list.push(result_increase[i]);
    temp_list.push(result_sum_list[i]-result_increase[i]);
    item_list.push(temp_list);
    console.log(temp_list[0]);
}