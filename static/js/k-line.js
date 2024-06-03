var mChart = echarts.init(document.getElementById('morris-bar-stacked'));
var bgColor = "#fff";//背景
var upColor="#F9293E";//涨颜色
var downColor="#00aa3b";//跌颜色

// ma  颜色
var ma5Color = "#39afe6";
var ma10Color = "#da6ee8";
var ma20Color = "#ffab42";
var ma30Color = "#00940b";



/**
 * 15:20 时:分 格式时间增加num分钟
 * @param {Object} time 起始时间
 * @param {Object} num
 */
function addTimeStr(time,num){ 
	var hour=time.split(':')[0];
	var mins=Number(time.split(':')[1]);
	var mins_un=parseInt((mins+num)/60);
	var hour_un=parseInt((Number(hour)+mins_un)/24);
	if(mins_un>0){
		if(hour_un>0){
			var tmpVal=((Number(hour)+mins_un)%24)+"";
			hour=tmpVal.length>1? tmpVal:'0'+tmpVal;//判断是否是一位
		}else{
			var tmpVal=Number(hour)+mins_un+"";
			hour=tmpVal.length>1? tmpVal:'0'+tmpVal;
		}
		var tmpMinsVal=((mins+num)%60)+"";
		mins=tmpMinsVal.length>1? tmpMinsVal:0+tmpMinsVal;//分钟数为 取余60的数
	}else{
		var tmpMinsVal=mins+num+"";
		mins=tmpMinsVal.length>1? tmpMinsVal:'0'+tmpMinsVal;//不大于整除60
	} 
	return hour+":"+mins;
}

//获取增加指定分钟数的 数组  如 09:30增加2分钟  结果为 ['09:31','09:32'] 
function getNextTime(startTime, endTIme, offset, resultArr) {
	var result = addTimeStr(startTime, offset);
	resultArr.push(result);
	if (result == endTIme) {
		return resultArr;
	} else {
		return getNextTime(result, endTIme, offset, resultArr);
	}
}


/**
 * 不同类型的股票的交易时间会不同  
 * @param {Object} type   hs=沪深  us=美股  hk=港股
 */
var time_arr = function(type) { 
	if(type.indexOf('us')!=-1){//生成美股时间段
		var timeArr = new Array();
		timeArr.push('09:30')
		return getNextTime('09:30', '16:00', 1, timeArr);
	}
	if(type.indexOf('hs')!=-1){//生成沪深时间段
		var timeArr = new Array();
			timeArr.push('09:30');
			timeArr.concat(getNextTime('09:30', '11:29', 1, timeArr)); 
			timeArr.push('13:00');
			timeArr.concat(getNextTime('13:00', '15:00', 1, timeArr)); 
		return timeArr;
	}
	if(type.indexOf('hk')!=-1){//生成港股时间段
		var timeArr = new Array();
			timeArr.push('09:30');
			timeArr.concat(getNextTime('09:30', '11:59', 1, timeArr)); 
			timeArr.push('13:00');
			timeArr.concat(getNextTime('13:00', '16:00', 1, timeArr)); 
		return timeArr;
	}
	
}


var get_m_data = function(m_data,type) {
	var priceArr = new Array();
	var avgPrice = new Array();
	var vol = new Array();
	var times = time_arr(type); 
	$.each(m_data.data, function(i, v) {
		priceArr.push(v[1]);
		avgPrice.push(v[2]);
		vol.push(v[3]); 
	})
	return {
		priceArr: priceArr,
		avgPrice: avgPrice,
		vol: vol,
		times: times
	}
}



//==========================================分时表 option

/**
 * 生成分时option 
 * @param {Object} m_data 分时数据
 * @param {Object} type 股票类型  us-美股  hs-沪深  hk-港股
 */




/**
 * 计算价格涨跌幅百分比
 * @param {Object} price 当前价
 * @param {Object} yclose 昨收价
 */
function ratioCalculate(price,yclose){
	return ((price-yclose)/yclose*100).toFixed(3);
}

//数组处理
function splitData(rawData) {
	var datas = []; var times = [];var vols = []; 
	for (var i = 0; i < rawData.length; i++) {
		datas.push(rawData[i]);
		times.push(rawData[i].splice(0, 1)[0]);
		vols.push(rawData[i][4]); 
	}
	return {datas:datas,times:times,vols:vols};
}


//================================MA计算公式
function calculateMA(dayCount,data) {
	var result = [];
	for (var i = 0, len = data.times.length; i < len; i++) {
		if (i < dayCount) {
			result.push('-');
			continue;
		}
		var sum = 0;
		for (var j = 0; j < dayCount; j++) {
			sum += data.datas[i - j][1];
		}
		result.push((sum / dayCount).toFixed(2));
	}
	return result;
}


//=================================================MADC计算公式

var calcEMA,calcDIF,calcDEA,calcMACD;

/*
 * 计算EMA指数平滑移动平均线，用于MACD
 * @param {number} n 时间窗口
 * @param {array} data 输入数据
 * @param {string} field 计算字段配置
 */
calcEMA=function(n,data,field){
    var i,l,ema,a;
    a=2/(n+1);
    if(field){
        //二维数组
        ema=[data[0][field]];  
        for(i=1,l=data.length;i<l;i++){
            ema.push((a*data[i][field]+(1-a)*ema[i-1]).toFixed(2));
        }
    }else{
        //普通一维数组
        ema=[data[0]];
        for(i=1,l=data.length;i<l;i++){
            ema.push((a*data[i]+(1-a)*ema[i-1]).toFixed(3) );
        }
    } 
    return ema;
};

/*
 * 计算DIF快线，用于MACD
 * @param {number} short 快速EMA时间窗口
 * @param {number} long 慢速EMA时间窗口
 * @param {array} data 输入数据
 * @param {string} field 计算字段配置
 */
calcDIF=function(short,long,data,field){
    var i,l,dif,emaShort,emaLong;
    dif=[];
    emaShort=calcEMA(short,data,field);
    emaLong=calcEMA(long,data,field);
    for(i=0,l=data.length;i<l;i++){
        dif.push((emaShort[i]-emaLong[i]).toFixed(3));
    }
    return dif;
};

/*
 * 计算DEA慢线，用于MACD
 * @param {number} mid 对dif的时间窗口
 * @param {array} dif 输入数据
 */
calcDEA=function(mid,dif){
    return calcEMA(mid,dif);
};

/*
 * 计算MACD
 * @param {number} short 快速EMA时间窗口
 * @param {number} long 慢速EMA时间窗口
 * @param {number} mid dea时间窗口
 * @param {array} data 输入数据
 * @param {string} field 计算字段配置
 */
calcMACD=function(short,long,mid,data,field){
    var i,l,dif,dea,macd,result;
    result={};
    macd=[];
    dif=calcDIF(short,long,data,field);
    dea=calcDEA(mid,dif);
    for(i=0,l=data.length;i<l;i++){
        macd.push(((dif[i]-dea[i])*2).toFixed(3));
    }
    result.dif=dif;
    result.dea=dea;
    result.macd=macd;
    return result;
};
 
 
 //=================================================MADC计算公式 end


  



function initMOption(cdata){
var data = splitData(cdata);
	var macd=calcMACD(12,26,9,data.datas,1);
	return {
			tooltip: { //弹框指示器
				trigger: 'axis',
				axisPointer: {
					type: 'cross'
				}
			},
			legend: { //图例控件,点击图例控制哪些系列不显示
				
				animation:true,
				textStyle: {
					fontSize: 12,
				},
			},
			axisPointer: {
				show: true
			},
			color: [ma5Color, ma10Color, ma20Color, ma30Color],
			grid: [{
				id: 'gd1',
				left: '5%',
				right: '1%',
				height: '55%', //主K线的高度,
				top: '10%'
			}, {
				left: '5%',
				right: '1%',
				top: '66.5%',
				height: '10%' //交易量图的高度
			}, {
				left: '5%',
				right: '1%',
				top: '80%', //MACD 指标
				height: '14%'
			}],
			xAxis: [ //==== x轴
				{ //主图
					type: 'category',
					data: data.times,
					scale: true,
					boundaryGap: false,
					axisLine: {
						onZero: false
					},
					axisLabel: { //label文字设置
						show: false
					},
					splitLine: {
						show: false,
						lineStyle: {
							color: '#3a3a3e'
						}
					},
					splitNumber: 20,
					min: 'dataMin',
					max: 'dataMax'
				}, { //交易量图
					type: 'category',
					gridIndex: 1,
					data: data.times,
					axisLabel: { //label文字设置
						color: '#404040',
						fontSize: 10
					},
				}, { //幅图
					type: 'category',
					gridIndex: 2,
					data: data.times,
					axisLabel: {
						show: false
					}
				}
			],
			yAxis: [ //y轴
				{ //==主图
					scale: true,
					z:-1,
					axisLabel: { //label文字设置
						color: '#404040'
						//label文字朝内对齐
					},
					splitArea: {
						show: true //显示分割区域
					   }

				}, { //交易图
					gridIndex: 1, splitNumber: 3, z:4,
					axisLine: {
						onZero: false
					},
					axisTick: {
						show: false
					},
					splitLine: {
						show: false
					},
					axisLabel: { //label文字设置
						color: '#c7c7c7',
						//label文字朝内对齐 
						fontSize: 8
					},
				}, { //幅图
					z:4, gridIndex: 2,splitNumber: 4,
					axisLine: {
						onZero: false
					},
					axisTick: {
						show: false
					},
					splitLine: {
						show: false
					},
					axisLabel: { //label文字设置
						color: '#c7c7c7',
						//label文字朝内对齐 
						fontSize: 8
					},
				}
			],
			dataZoom: [
				{
					filterMode:'filter', //当前数据窗口外的数据被过滤掉来达到数据窗口缩放的效果 默认值filter
					type: 'inside', //内置型数据区域缩放组件
					start: 50, //数据窗口范围的起始百分比
					end: 100 //数据窗口范围的结束百分比
				   },
				
				{
					type: 'slider',
					xAxisIndex: [0, 1, 2], //控件联动
					start: 50,
					end: 100,
					throttle: 10,
					top: '94%',
					height: '6%',
					handleSize: '90%', //滑块图标
					handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
					dataBackground: {
						lineStyle: {
							color: '#fff'
						}, //数据边界线样式
						areaStyle: {
							color: '#696969'
						} //数据域填充样式
					}
				},
				// 		{
				// 			type: 'inside',
				// 			xAxisIndex: [0,1,2],//控件联动
				// 		},
			],
			animation: false, //禁止动画效果
			backgroundColor: bgColor,
			blendMode: 'source-over',
			series: [
				{
			name: '日K',
			type: 'candlestick', //K线图
			data: data.datas, //y轴对应的数据
			////////////////////////图标标注/////////////////////////////
			markPoint: { //图表标注
			label: { //标注的文本
				normal: { //默认不显示标注
				show:true,
				//position:['20%','30%'],
				formatter: function (param) { //标签内容控制器
				return param != null ? Math.round(param.value) : '';
				}
				}
			},
			data: [ //标注的数据数组
				{
				name: 'XX标点',
				coord: ['2013/5/31', 2300], //指定数据的坐标位置
				value: 2300,
				itemStyle: { //图形样式
				normal: {color: 'rgb(41,60,85)'}
				}
				},
				{
				name: 'highest value',
				type: 'max', //最大值
				valueDim: 'highest' //在highest维度上的最大值 最高价
				},
				{
				name: 'lowest value',
				type: 'min',
				valueDim: 'lowest' //最低价
				},
				{
				name: 'average value on close',
				type: 'average',
				valueDim: 'close' //收盘价
				}
			],
			tooltip: { //提示框
				formatter: function (param) {
				return param.name + '<br>' + (param.data.coord || '');
				}
			}
			},
			/////////////////////////////////图标标线///////////////////////////
			markLine: {
			symbol: ['none', 'none'], //标线两端的标记类型
			data: [
				[
				{
				name: 'from lowest to highest',
				type: 'min', //设置该标线为最小值的线
				valueDim: 'lowest', //指定在哪个维度上的最小值
				symbol: 'circle',
				symbolSize: 10, //起点标记的大小
				label: { //normal默认，emphasis高亮
				normal: {show: false}, //不显示标签
				emphasis: {show: false} //不显示标签
				}
				},
				{
				type: 'max',
				valueDim: 'highest',
				symbol: 'circle',
				symbolSize: 10,
				label: {
				normal: {show: false},
				emphasis: {show: false}
				}
				}
				],
			
				{
				name: 'min line on close',
				type: 'min',
				valueDim: 'close'
				},
				{
				name: 'max line on close',
				type: 'max',
				valueDim: 'close'
				}
			]
			
			}
			
			},
			{ //MA5 5天内的收盘价之和/5
				name: 'MA5',
				type: 'line',
				data: calculateMA(5,data),
				smooth: true,
				lineStyle: {
				normal: {opacity: 0.5}
				}
			},
				{
					name: 'MA10',
					type: 'line',
					data: calculateMA(10,data),
					smooth: true,
					lineStyle: { //标线的样式
					normal: {opacity: 0.5}
					}
				   },

				{
					name: 'MA20',
					type: 'line',
					data: calculateMA(20,data),
					smooth: true,
					lineStyle: {
					normal: {opacity: 0.5}
					}
				},
				{
					name: 'MA30',
					type: 'line',
					data: calculateMA(30,data),
					smooth: true,
					lineStyle: {
					normal: {opacity: 0.5}
					}
				   },
				   {
					name: 'Volumn',
					type: 'bar',
					xAxisIndex: 1,
					yAxisIndex: 1,
					data: data.vols,
					barWidth: '60%',
					itemStyle: {
						normal: {
							color: function(params) {
								var colorList;
								if (data.datas[params.dataIndex][1] > data.datas[params.dataIndex][0]) {
									colorList = upColor;
								} else {
									colorList = downColor;
								}
								return colorList;
							},
						}
					}
				},
				{
					name: 'MACD',
					type: 'bar',
					xAxisIndex: 2,
					yAxisIndex: 2,
					data: macd.macd,
					barWidth: '40%',
					itemStyle: {
						normal: {
							color: function(params) {
								var colorList;
								if (params.data >= 0) {
									colorList = upColor;
								} else {
									colorList = downColor;
								}
								return colorList;
							},
						}
					}
				}, {
					name: 'DIF',
					type: 'line',
					symbol: "none",
					xAxisIndex: 2,
					yAxisIndex: 2,
					data: macd.dif,
					lineStyle: {
						normal: {
							color: '#da6ee8',
							width: 1
						}
					}
				}, {
					name: 'DEA',
					type: 'line',
					symbol: "none",
					xAxisIndex: 2,
					yAxisIndex: 2,
					data: macd.dea,
					lineStyle: {
						normal: {
							opacity: 0.8,
							color: '#39afe6',
							width: 1
						}
					}
				}
				




			]
		};
		
		
}

mChart.setOption(initMOption(kdata)); 



