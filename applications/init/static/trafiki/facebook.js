Facebook = (function(){
    var _self;
    return _self = Ext.extend(Widget, {		
		getPoint: function(callback, type){
			app.fireEvent('open', new FacebookView({
				type: type,
				callback: callback
			}));
		}
	})
})();