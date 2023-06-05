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
	input wire A,
	input wire B,
	input wire Ki,
	output wire gi,
   output wire hi,
   output wire pi,
   output wire api,
	output wire bpi1
);
	reg gi_or_bi1_ifk0;
   reg ai_ifk1;
   reg hi_or_ai_ifk0;
   reg pi_or_bi1_ifk1;
	reg api_out;
	reg bpi_out;
	
	always @(*) begin
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
	input wire A_i,
	input wire B_i_prev,
	output wire gi_prim,
   output wire hi_prim,
   output wire pi_prim
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

module HashedCellRow(
	input wire [WIDTH-1:0] A_vector,
	input wire [WIDTH-1:0] B_vector,
	input wire [WIDTH-1:0] K_vector,
	output wire [WIDTH-1:0] gi_v,
	output wire [WIDTH-1:0] hi_v,
	output wire [WIDTH-1:0] pi_v,
	output wire [WIDTH-1:0] api_v,
	output wire [WIDTH-1:0] bpi1_v
);
	parameter WIDTH = 7;
	
	genvar i;
	generate
		for(i=0; i<WIDTH; i=i+1) begin: h_caell_gen
		HashedCell hcell_status(
			.A(A_vector[i]),
			.B(B_vector[i]),
			.Ki(K_vector[i]),
			.gi(gi_v[i]),
			.hi(hi_v[i]),
			.pi(pi_v[i]),
			.api(api_v[i]),
			.bpi1(bpi1_v[i])
		);
		end
	endgenerate
endmodule
//////////////////////////////////////////////////////////////////////////////////
module main;
 parameter N_bits = 7;
    assign stages = $clog2(N_bits);
    wire [N_bits-1:0] A_vector = 7'd69;
    wire [N_bits-1:0] B_vector = 7'd45;
    wire [N_bits-1:0] K_vector = 7'd20;
    
    wire [N_bits-1:0] gi;
    wire [N_bits-1:0] hi;
    wire [N_bits-1:0] pi;
    wire [N_bits-1:0] api;
    wire [N_bits-1:0] bpi1;
	 
	 HashedCellRow #(.WIDTH(N_bits)) hr(.A_vector(A_vector), .B_vector(B_vector), .K_vector(K_vector),
	 .gi_v(gi), .hi_v(hi), .pi_v(pi), .api_v(api), .bpi1_v(bpi1));
    
    initial begin
        #1 $display("a = %b", A_vector);
        #1 $display("b = %b", B_vector);
        #1 $display("k = %b", K_vector);
        #1 $display("g = %b", gi);
    end
endmodule
