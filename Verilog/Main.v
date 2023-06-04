`timescale 1ns / 1ps
////////////////////////////////////////////////////////////////////////////////// 
// Design Name: 
// Module Name:    Main 
// Project Name:	 Modular Adder
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module HashedCell(
	input A,
	input B,
	input Ki,
	output gi,
   output hi,
   output pi,
   output api,
	output bpi1
);
	reg gi_or_bi1_ifk0;
   reg ai_ifk1;
   reg hi_or_ai_ifk0;
   reg pi_or_bi1_ifk1;
	reg api_out;
	reg bpi_out;
	
	initial begin
		gi_or_bi1_ifk0 = A & B;
		ai_ifk1 = (A & B) | (( ~A ) & ( ~B ));
		hi_or_ai_ifk0 = A ^ B;
		pi_or_bi1_ifk1 = A | B;
	end
	always @(*) begin 
		if(Ki)
			api_out = ai_ifk1;
		else
			api_out = hi_or_ai_ifk0;
	end
	always @(*) begin
		if(Ki)
			bpi_out = pi_or_bi1_ifk1;
		else
			bpi_out = gi_or_bi1_ifk0;
	end
	
	assign gi = gi_or_bi1_ifk0;
	assign hi = hi_or_ai_ifk0;
	assign pi = pi_or_bi1_ifk1;
	assign api = api_out;
	assign bpi1 = bpi_out;
endmodule

module EnvelopedCell(
	input A_i,
	input B_i_prev,
	output gi_prim,
   output hi_prim,
   output pi_prim
);
	assign gi_prim = A_i & B_i_prev;
   assign hi_prim = A_i ^ B_i_prev;
   assign pi_prim = A_i | B_i_prev;
endmodule

module PrefixAdderCell(
	input Gi_input,
	input Gi_prev_input,
	input Pi_input,
	input Pi_prev_input,
	output pi_out,
   output gi_out
);
	assign pi_out = Pi_input & Pi_prev_input;
   assign gi_out = Gi_input | (Gi_prev_input & Pi_input);
endmodule

module DelayCell(
	input Pi,
   input Gi,
   input Pi_prim,
   input Gi_prim,
	output pi,
   output gi,
   output pi_prim,
   output gi_prim
);
	buf(pi, Pi);
	buf(gi, Gi);
	buf(pi_prim, Pi_prim);
	buf(gi_prim, gi_prim);
endmodule

//////////////////////////////////////////////////////////////////////////////////
module Main;
	parameter N_bit = 7;
	
	initial begin
		$display("Hello");
	end
endmodule
