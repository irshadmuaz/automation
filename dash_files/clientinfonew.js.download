var _GRAPH_LOADER = 'wv-graph-loader wv-loader wv-loader--center';
var clientTrendGraph;
var graph;
// When the user clicks anywhere outside of the wvgraph modal pop up, close it
$(document).ready(function(){
	clientTrendGraph = $('.wvgraph-clientTrendgraph');

	graph = $('#trendingGraph');
	
	$('.wvgraph-content-table-cell').click(function()
	{
		graph.hide();
		$(document).off('keyup');
	});	
});


function showGraphLoading()
{
	graph.show();
	clientTrendGraph.addClass(_GRAPH_LOADER);	
}

function hideGraphLoading()
{
	clientTrendGraph.removeClass(_GRAPH_LOADER);
}

function getVitalNameByType(vitalType)
{
	var vitalMapping = {
		1:"weights",
		2:"respiration",
		3:"bloodPressure",
		5:"temperature",
		6:"pulse",
		7:"bloodSugar",
		8:"heights",
		9:"o2Sats",
		10:"painLevel"
	};
	var mapKey = vitalMapping[vitalType];
	return window.clientInfoGraph.moduleProps.vitalMap[mapKey];
}

function renderGraph(data, vitalType)
{
	var _chart = {},
		chartOpts,
		baseLineOpts = [],
		localChartOpts = {},
		maxValue = -99999,
		minValue = 99999;
	
	if(data.vitalList)
	{
		if (vitalType >= 0 && vitalType < window.clientInfoGraph.moduleProps.chartOpts.length) {
			localChartOpts = window.clientInfoGraph.moduleProps.chartOpts[vitalType];
		}

		chartOpts = $.extend(true, {}, localChartOpts, window.clientInfoGraph.moduleProps.defaultChartOpts);
		
		if (data.baseline) {
			baseLineOpts.push.apply(baseLineOpts, [{
			    value : data.baseline,
			    class: 'pccChartBaselineSystolic'}, 
				{ value : data.baseline, 
				text : vitalType === 3 ? window.clientInfoGraph.moduleProps.termMap.systolicBaseline : window.clientInfoGraph.moduleProps.termMap.baseline,
				position : 'start',
				class: 'pccChartBaselineSystolic',
			}]);
			maxValue = Math.max(maxValue, data.baseline);
			minValue = Math.min(minValue, data.baseline);
		}

		if (data.diastolicBaseline) { // Should only be true when vitalType
										// === 3 (Blood Pressure)
			baseLineOpts.push.apply(baseLineOpts, [{
			    value : data.diastolicBaseline,
			    class: 'pccChartBaselineDiastolic'},
				{ value : data.diastolicBaseline,
				text : window.clientInfoGraph.moduleProps.termMap.diastolicBaseline,
				position : 'start',
				class: 'pccChartBaselineDiastolic',
			}]);
			maxValue = Math.max(maxValue, data.diastolicBaseline);
			minValue = Math.min(minValue, data.diastolicBaseline);			
		}

		data.vitalList.forEach(function(elem) {
			chartOpts.data.columns[0].push(elem.value);
			maxValue = Math.max(maxValue, elem.value);
			minValue = Math.min(minValue, elem.value);
			if (vitalType === 3) {
				 // Blood pressure also has the dystolicValue
				chartOpts.data.columns[1].push(elem.diastolicValue);
				maxValue = Math.max(maxValue, elem.diastolicValue);
				minValue = Math.min(minValue, elem.diastolicValue);				
			}
		});

		chartOpts.axis.y = {
				min : minValue,
				max : maxValue,
		};
		
		// setup the format for non-integer values
		if (vitalType === 1 || vitalType === 5 || vitalType === 7 || vitalType === 9)
		{
			chartOpts.axis.y.tick = {
				format : function (x) { return d3.format('.1f')(x);},
			};
		}
		else
		{
			chartOpts.axis.y.tick = {
				format : function (x) { return d3.format('d')(x);},
			};
		}

		_chart = clientTrendGraph.pccGenerateChart(chartOpts, getVitalNameByType(vitalType), undefined, '');

		_chart.load({columns : chartOpts.data.columns});

		if (baseLineOpts.length > 0) {
			_chart.ygrids(baseLineOpts);
		}
	}
	else
	{
		clientTrendGraph.html("<p>No Data Available Within 90 Days.</p>");
	}	
}

function openExceptionTrendingGraph(clientId, vitalType)
{
	// clean up the former data
	clientTrendGraph.empty();
	showGraphLoading();
	$.getJSON('/clinical/alerts/smart/getwvhistory.xhtml', {
		clientId : clientId,
		wvType : vitalType
	})
	.done(function (data) {
		renderGraph(data, vitalType);
		hideGraphLoading();
	})
	.fail(function (data) {		
		clientTrendGraph.html("<p>Failed To Load Data.</p>");
		hideGraphLoading();
	});
	$(document).on('keyup',function(e) {
	    if(e.which === 27) {
	    	graph.hide();
	    	$(document).off('keyup');
	    }
	});
}
