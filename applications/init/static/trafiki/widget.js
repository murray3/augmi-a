Widget = (function(){
    var _self;
    return _self = Ext.extend(Ext.Button, {
		tpl: new Ext.XTemplate([
            '<div class="outerWrapper"><div class="innerWrapper x-button x-button-plain"><img class="x-icon-mask icon {icon}" /><div class="title">{title}</div></div></div>'
        ]),
		
		initComponent: function(){
			this.html = this.tpl.apply(this.o);
			_self.superclass.initComponent.call(this);
		},
		
		pressedCls: 'pressed',
		pressedDelay: 100,
		baseCls: 'widget',
		
		getPoint: function(callback){
			callback(null, this.o);
		},
		
		onTap: function(){
			var me = this;
			async.series([this.getPoint.bind(this)], function(err, results){
				app.fireEvent('open', new StopView({
					o: results[0],
					widget: me
				}));
			});
			/*Ext.defer(function(){
				app.fireEvent('open', new SearchView());
			}, 1);*/
		}

	})
})();