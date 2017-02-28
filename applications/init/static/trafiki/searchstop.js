SearchStop = (function(){
    var _self;
    return _self = Ext.extend(Widget, {		
		getPoint: function(callback, type){
			console.log('type', type);
			//console.log(callback);
			app.fireEvent('open', new SearchView({ 
			    type: type,
				callback: callback 
			}));
		}
	})
})();