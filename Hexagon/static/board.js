var colors = {
	0: "#DDDDDD",
	1: "red",
	2: "blue"
};

$( document ).ready( function() {
	
	if ( typeof board === "undefined" ) {
		alert( "Unable to find board!" );
		return;
	}
	
	if ( typeof playerNum === "undefined" ) {
		alert( "Cound not find player number" );
		return;
	}
	
	// Determine which color the clicked square should be
	var playerColor = colors[ playerNum ];
	
	var clickedOnce = false;
	
	var stage = new Kinetic.Stage( {
		container: "game-board",
		width: 800,
		height: 500
	} );

	var layer = new Kinetic.Layer();

	for ( var rownum = 0; rownum < 10; rownum++ ) {

		var yPos = 50 + 2 * rownum * 22;

		for ( var colnum = 0; colnum < 10; colnum++ ) {

			var xPos = 50 + 2 * colnum * 26 + rownum * 26;

			var squareState = board[ rownum ][ colnum ];
			color = colors[ squareState ];

			var hex = new Kinetic.RegularPolygon( {
				x: xPos,
				y: yPos,
				sides: 6,
				radius: 30,
				fill: color,
				stroke: "black",
				strokeWidth: 2,
				draggable: false
			} );
			
			hex.locked = ( squareState !== 0 );
			hex.row = rownum;
			hex.col = colnum;
			
			hex.on( "mouseover", function() {
				if ( this.locked === true ) {
					return;
				}
				
				this.setFill( "yellow" );
				layer.draw();
			} );

			hex.on( "mouseout", function() {
				if ( this.locked === true ) {
					return;
				}

				this.setFill( color );
				layer.draw();
			} );
			
			hex.on( "click", function() {
				if ( this.locked === true ) {
					return;
				}
				
				if ( clickedOnce === true ) {
					return;
				}

				this.locked = true;
				clickedOnce = true;
				
				// Set values to be sent back to server
				$( "#row" ).val( this.row );
				$( "#col" ).val( this.col );

				var that = this;
				this.transitionTo( {
					scale: {
						x: 0
					},
					duration: 0.25,
					easing: "linear",
					callback: function() {
						that.setFill( playerColor );
						layer.draw();
						
						that.transitionTo( {
							scale: {
								x: 1.0
							},
							easing: "linear",
							duration: 0.25
						} );
					}
				} );
			} );
		
			layer.add( hex );
		}
	}

	stage.add(layer);
} );
