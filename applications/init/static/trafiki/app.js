App = (function(){
	var _self;
	return _self = Ext.extend(Ext.Panel, {
		title: 'Trafiki',
		fullscreen: true,
		layout: 'card',
		initComponent: function(){
			var me = this;
			this.backButton = new NavButton({
	            text: "Back",
	            ui: 'back',
	            handler: this.onBack,
	            hidden: true,
	            scope: this,
				onTaphold: function(){
					me.onBack(null, null, me.windowStack[0]);
				}
	        });
			
			this.navigationBar = new Ext.Toolbar({
	            ui: 'dark',
	            dock: 'top',
	            title: this.title || "",
	            items: [this.backButton, {xtype: 'spacer'}]
	        });
			
			this.dockedItems = [this.navigationBar];
			
			this.windowStack = [];
			this.addEvents('open');
			
			this.listeners = {
				open: this.onOpen
			};
			
			_self.superclass.initComponent.call(this);
		},		
		
		onOpen: function(win){
			var first = this.windowStack.length == 0;
			this.windowStack.push(win);
			first ? this.setCard(win) : this.setCard(win, { type: 'slide', reverse: false });
	
			this.backButton.setText(win.backButtonTitle || (this.currentWindow || {}).title || "Back");
			this.navigationBar.setTitle(win.title || "");
			!first && this.backButton.show();
			
			(this.currentWindow || {}).rightNavButton && this.navigationBar.remove(this.currentWindow.rightNavButton);
			win.rightNavButton && this.navigationBar.add(win.rightNavButton = new win.rightNavButton.constructor(win.rightNavButton.initialConfig));
			(win.rightNavButton || (this.currentWindow || {}).rightNavButton) && this.navigationBar.doLayout();
			
			this.currentWindow = win;
		},
		
		onBack: function(el, e, toWin){
			var win = this.windowStack[this.windowStack.length - 1];
			win && win.onBack && win.onBack();
			
			var winBefore = toWin || this.windowStack[this.windowStack.length - 2];
			if(!winBefore){ return; }
			this.windowStack.splice(this.windowStack.indexOf(winBefore) + 1);
			
	        this.setCard(winBefore, {
	            type: 'slide',
	            reverse: true
	        });

			this.backButton.setText(winBefore.backButtonTitle || (this.windowStack[this.windowStack.indexOf(winBefore) - 1] || {}).title || "Back");
			this.navigationBar.setTitle(winBefore.title || "");
			if(this.windowStack.length == 1){ this.backButton.hide(); }
		
			win.rightNavButton && this.navigationBar.remove(win.rightNavButton);
			winBefore.rightNavButton && this.navigationBar.add(winBefore.rightNavButton = new winBefore.rightNavButton.constructor(winBefore.rightNavButton.initialConfig)); //Screwed up, but couldn't get around rendering destroyed objects, and couldn't remove without destroying
			try { (win.rightNavButton || winBefore.rightNavButton) && this.navigationBar.doLayout(); } catch(e){ console.error(e); }
			
			this.currentWindow = winBefore;
		},
		
		getRoute: function(points){
			async.series(
				points.map(function(item, i, arr){ 
					return Ext.createDelegate(item.getPoint, item, [i == 0 ? 'from' : (i == arr.length - 1 ? 'to' : 'via')], true ); 
				}), 
				
				function(err, res){
					//console.log('res', res);
					app.fireEvent('open', new RouteView({ points: res }));
				}
			);
		}
	});
})();