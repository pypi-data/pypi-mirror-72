digraph {
	compound = "true"
	newrank = "true"
	subgraph "root" {
		"[root] aws_elb.web" [label = "aws_elb.web", shape = "box"]
		"[root] aws_instance.web" [label = "aws_instance.web", shape = "box"]
		"[root] aws_internet_gateway.gw" [label = "aws_internet_gateway.gw", shape = "box"]
		"[root] aws_lb_cookie_stickiness_policy.default" [label = "aws_lb_cookie_stickiness_policy.default", shape = "box"]
		"[root] aws_route_table.r" [label = "aws_route_table.r", shape = "box"]
		"[root] aws_route_table_association.a" [label = "aws_route_table_association.a", shape = "box"]
		"[root] aws_security_group.default" [label = "aws_security_group.default", shape = "box"]
		"[root] aws_security_group.elb" [label = "aws_security_group.elb", shape = "box"]
		"[root] aws_subnet.tf_test_subnet" [label = "aws_subnet.tf_test_subnet", shape = "box"]
		"[root] aws_vpc.default" [label = "aws_vpc.default", shape = "box"]
		"[root] output.address" [label = "output.address", shape = "note"]
		"[root] provider.aws" [label = "provider.aws", shape = "diamond"]
		"[root] var.aws_amis" [label = "var.aws_amis", shape = "note"]
		"[root] var.aws_region" [label = "var.aws_region", shape = "note"]
		"[root] var.key_name" [label = "var.key_name", shape = "note"]
		"[root] aws_elb.web" -> "[root] aws_instance.web"
		"[root] aws_elb.web" -> "[root] aws_security_group.elb"
		"[root] aws_instance.web" -> "[root] aws_security_group.default"
		"[root] aws_instance.web" -> "[root] aws_subnet.tf_test_subnet"
		"[root] aws_instance.web" -> "[root] var.aws_amis"
		"[root] aws_instance.web" -> "[root] var.key_name"
		"[root] aws_internet_gateway.gw" -> "[root] aws_vpc.default"
		"[root] aws_lb_cookie_stickiness_policy.default" -> "[root] aws_elb.web"
		"[root] aws_route_table.r" -> "[root] aws_internet_gateway.gw"
		"[root] aws_route_table_association.a" -> "[root] aws_route_table.r"
		"[root] aws_route_table_association.a" -> "[root] aws_subnet.tf_test_subnet"
		"[root] aws_security_group.default" -> "[root] aws_vpc.default"
		"[root] aws_security_group.elb" -> "[root] aws_internet_gateway.gw"
		"[root] aws_subnet.tf_test_subnet" -> "[root] aws_vpc.default"
		"[root] aws_vpc.default" -> "[root] provider.aws"
		"[root] meta.count-boundary (EachMode fixup)" -> "[root] aws_lb_cookie_stickiness_policy.default"
		"[root] meta.count-boundary (EachMode fixup)" -> "[root] aws_route_table_association.a"
		"[root] meta.count-boundary (EachMode fixup)" -> "[root] output.address"
		"[root] output.address" -> "[root] aws_elb.web"
		"[root] provider.aws (close)" -> "[root] aws_lb_cookie_stickiness_policy.default"
		"[root] provider.aws (close)" -> "[root] aws_route_table_association.a"
		"[root] provider.aws" -> "[root] var.aws_region"
		"[root] root" -> "[root] meta.count-boundary (EachMode fixup)"
		"[root] root" -> "[root] provider.aws (close)"
	}
}


