View = (function(){
	var _self;
	return _self = Ext.extend(Ext.Panel, {
		listeners: {
			deactivate: function(){ this.items && this.items.items && this.items.items.length && this.items.items.forEach(function(item){ item.fireEvent('deactivate'); }); }
		},
		layout: {
			type: 'vbox',
			align: 'stretch'
		},
		initComponent: function(){
			_self.superclass.initComponent.call(this);
		},
		scroll: false
	});
})();
