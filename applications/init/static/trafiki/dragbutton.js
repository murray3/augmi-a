DragButton = (function(){
	var _self;
	return _self = Ext.extend(Ext.Button, {
		touched: false,
		stepping: false,
		step: 10,
		ui: 'action',
		cls: 'dragbutton',
		iconMask: true,
		iconCls: 'code2',
		iconAlign: 'left',
		
		initComponent: function(){
			this.addEvents('stepstart', 'step', 'stepend');
			_self.superclass.initComponent.call(this);
		},
		
		afterRender: function(){
			_self.superclass.afterRender.call(this);
			
			this.helpPanel = new Ext.Panel({
				cls: 'helper',
				floating: true,
				width: 120,
				height: 60,
				html: 'Drag horizontally to quickly change date',
				styleHtmlContent: true,
			});
		},
		
		initEvents: function(){
			var me = this;
			
			this.ownerCt.mon(this.ownerCt.el, {
				scope: me,
				touchmove  : me.onTouchMove,
			});
			
			me.mon(me.el, {
	            scope: me,
	            touchstart : me.onTouchStart,
	            touchend   : me.onTouchEnd
	        });
			_self.superclass.initEvents.call(this);
		},
		
		onTouchStart: function(){
			this.touched = true;
			this.fireEvent('stepstart');
		},
		
		onTouchMove: function(e, el){
			if(this.touched){
				if(!this.stepping){
					this.stepping = true;
					this.helpPanel.showBy(this.el, 'fade');
				}
				this.fireEvent('step', Math.round(e.deltaX / this.step));
			}
		},
		
		onTouchEnd: function(){
			this.fireEvent('stepend');
			this.touched = false;
			if(this.stepping){
				this.stepping = false;
				this.helpPanel.hide();
			}
		}
	});
})();
