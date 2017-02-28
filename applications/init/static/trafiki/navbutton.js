NavButton = (function(){
	var _self;
	return _self = Ext.extend(Ext.Button, {
		initEvents: function(){	
			var me = this;
			_self.superclass.initEvents.call(this);
			me.mon(me.el, {
	            scope: me,
				taphold: me.onTaphold
	        });
		}
	});
})();