import os
import sys
import hcl2
import subprocess
from collections import defaultdict

# Friendly descriptions for common AWS resources
RESOURCE_DESCRIPTIONS = {
    "aws_instance": "EC2 virtual machine instance",
    "aws_s3_bucket": "S3 storage bucket",
    "aws_vpc": "Virtual Private Cloud (network)",
    "aws_subnet": "Subnet inside a VPC",
    "aws_internet_gateway": "Internet Gateway for public internet access",
    "aws_route_table": "Route Table for directing network traffic",
    "aws_security_group": "Firewall rules for controlling inbound/outbound traffic",
    "aws_lb": "Load Balancer",
    "aws_lb_target_group": "Target group for Load Balancer",
    "aws_db_instance": "RDS Database instance",
    "aws_eks_cluster": "EKS Kubernetes cluster",
    "aws_lambda_function": "Serverless function (Lambda)",
    "aws_iam_role": "IAM Role for permissions",
    "aws_iam_policy": "IAM Policy defining access rules",
}

README_TEMPLATE = """# Terraform Project Documentation

## Overview
This project contains Terraform code to provision infrastructure.

---

## Providers
{providers}

---

## Modules
{modules}

---

## Resources
{resources}

---

## Variables
{variables}

---

## Outputs
{outputs}

---

## Architecture Diagram
![Terraform Architecture](architecture.png)

---
*Generated automatically from Terraform code.*
"""


def parse_tf_file(file_path):
    """Parse a Terraform .tf file and return its content as dict."""
    with open(file_path, "r") as f:
        return hcl2.load(f)


def extract_comments_map(file_path):
    """
    Extract comments and map them to the next Terraform block keyword.
    Returns: dict mapping resource/module/variable/output/provider names to comments.
    """
    comments_map = {}
    last_comment = None

    with open(file_path, "r") as f:
        for line in f:
            stripped = line.strip()

            # Capture comments
            if stripped.startswith("#") or stripped.startswith("//"):
                last_comment = stripped
                continue

            # Attach comment to following Terraform block line
            if last_comment:
                if stripped.startswith("resource"):
                    try:
                        parts = stripped.split()
                        res_type = parts[1].strip('"')
                        res_name = parts[2].strip('"').rstrip("{")
                        comments_map[f"resource.{res_type}.{res_name}"] = last_comment
                    except Exception:
                        pass

                elif stripped.startswith("module"):
                    try:
                        parts = stripped.split()
                        mod_name = parts[1].strip('"').rstrip("{")
                        comments_map[f"module.{mod_name}"] = last_comment
                    except Exception:
                        pass

                elif stripped.startswith("variable"):
                    try:
                        parts = stripped.split()
                        var_name = parts[1].strip('"').rstrip("{")
                        comments_map[f"variable.{var_name}"] = last_comment
                    except Exception:
                        pass

                elif stripped.startswith("output"):
                    try:
                        parts = stripped.split()
                        out_name = parts[1].strip('"').rstrip("{")
                        comments_map[f"output.{out_name}"] = last_comment
                    except Exception:
                        pass

                elif stripped.startswith("provider"):
                    try:
                        parts = stripped.split()
                        prov_name = parts[1].strip('"').rstrip("{")
                        comments_map[f"provider.{prov_name}"] = last_comment
                    except Exception:
                        pass

                last_comment = None

    return comments_map


def extract_info(tf_dir):
    """Extract providers, modules, resources, variables, outputs + comments from Terraform project."""
    providers = []
    modules = []
    resources_by_type = defaultdict(list)
    variables = []
    outputs = []

    comments_global = {}

    for root, _, files in os.walk(tf_dir):
        for file in files:
            if file.endswith(".tf"):
                file_path = os.path.join(root, file)

                # Collect comments mapped to entities
                comments_map = extract_comments_map(file_path)
                comments_global.update(comments_map)

                tf_data = parse_tf_file(file_path)

                # Extract providers
                if "provider" in tf_data:
                    for prov in tf_data["provider"]:
                        for prov_name, prov_details in prov.items():
                            comment = comments_global.get(f"provider.{prov_name}", "")
                            entry = f"- **{prov_name}**"
                            if comment:
                                entry += f" → {comment}"
                            providers.append(entry)

                # Extract modules
                if "module" in tf_data:
                    for mod in tf_data["module"]:
                        for mod_name, mod_details in mod.items():
                            comment = comments_global.get(f"module.{mod_name}", "")
                            source = mod_details.get("source", "N/A")
                            entry = f"- **{mod_name}** (source: `{source}`)"
                            if comment:
                                entry += f" → {comment}"
                            modules.append(entry)

                # Extract resources
                if "resource" in tf_data:
                    for res in tf_data["resource"]:
                        for res_type, res_blocks in res.items():
                            description = RESOURCE_DESCRIPTIONS.get(res_type, "Terraform resource")
                            header = f"- **{res_type}** → {description}"
                            if header not in resources_by_type[res_type]:
                                resources_by_type[res_type].append(header)
                            for res_name in res_blocks:
                                comment = comments_global.get(f"resource.{res_type}.{res_name}", "")
                                entry = f"  - **{res_name}**"
                                if comment:
                                    entry += f" → {comment}"
                                resources_by_type[res_type].append(entry)

                # Extract variables
                if "variable" in tf_data:
                    for var in tf_data["variable"]:
                        for var_name, var_details in var.items():
                            comment = comments_global.get(f"variable.{var_name}", "")
                            default_val = var_details.get("default", "No default")
                            desc = var_details.get("description", "No description")
                            entry = f"- **{var_name}** (default: `{default_val}`) → {desc}"
                            if comment:
                                entry += f" | {comment}"
                            variables.append(entry)

                # Extract outputs
                if "output" in tf_data:
                    for out in tf_data["output"]:
                        for out_name, out_details in out.items():
                            comment = comments_global.get(f"output.{out_name}", "")
                            desc = out_details.get("description", "No description")
                            entry = f"- **{out_name}** → {desc}"
                            if comment:
                                entry += f" | {comment}"
                            outputs.append(entry)

    return providers, modules, resources_by_type, variables, outputs


def format_resources(resources_by_type):
    """Format grouped resources into markdown."""
    if not resources_by_type:
        return "No resources defined."

    lines = []
    for res_type, res_list in sorted(resources_by_type.items()):
        lines.extend(res_list)
        lines.append("")  # spacing
    return "\n".join(lines)


def generate_architecture_diagram(tf_dir):
    """Generate architecture diagram using terraform graph + Graphviz."""
    dot_file = os.path.join(tf_dir, "architecture.dot")
    png_file = os.path.join(tf_dir, "architecture.png")

    try:
        subprocess.run(
            ["terraform", "graph"],
            cwd=tf_dir,
            stdout=open(dot_file, "w"),
            stderr=subprocess.PIPE,
            check=True,
        )
        subprocess.run(
            ["dot", "-Tpng", dot_file, "-o", png_file],
            check=True,
        )
        print(f"✅ Architecture diagram generated: {png_file}")
    except Exception as e:
        print(f"⚠️ Skipping architecture diagram (Terraform/Graphviz error: {e})")


def generate_readme(tf_dir, output_file="README.md"):
    providers, modules, resources_by_type, variables, outputs = extract_info(tf_dir)

    readme_content = README_TEMPLATE.format(
        providers="\n".join(providers) if providers else "No providers defined.",
        modules="\n".join(modules) if modules else "No modules defined.",
        resources=format_resources(resources_by_type),
        variables="\n".join(variables) if variables else "No variables defined.",
        outputs="\n".join(outputs) if outputs else "No outputs defined.",
    )

    with open(os.path.join(tf_dir, output_file), "w") as f:
        f.write(readme_content)

    print(f"✅ README.md generated at {os.path.join(tf_dir, output_file)}")

    # Generate diagram too
    generate_architecture_diagram(tf_dir)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_readme.py <terraform_project_folder>")
        sys.exit(1)

    tf_project_dir = sys.argv[1]
    if not os.path.exists(tf_project_dir):
        print(f"❌ Path not found: {tf_project_dir}")
        sys.exit(1)

    generate_readme(tf_project_dir)
