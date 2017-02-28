IconButton = (function(){
    var _self;
    return _self = Ext.extend(Ext.Button, {
		tpl: new Ext.XTemplate([
            '<div class="outerWrapper"><div class="innerWrapper"><div class="icon refresh"></div><div class="title">{title}</div></div></div>'
        ]),
		
		initComponent: function(){
			this.html = this.tpl.apply(this.o);
			_self.superclass.initComponent.call(this);
		},
		
		pressedCls: 'pressed',
		pressedDelay: 100,
		baseCls: 'widget',
		
		onTap: function(){
			console.log('tap');
			/*Ext.defer(function(){
				app.fireEvent('open', new SearchView());
			}, 1);*/
		}

	})
})();