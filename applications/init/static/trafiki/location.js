Location = (function(){
    var _self;
    return _self = Ext.extend(Widget, {		
		getPoint: function(callback){
			// Getting location here and injecting
			callback(null, { title: 'Here' });
		}
	})
})();