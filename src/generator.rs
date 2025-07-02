// src/generator.rs

use crate::config::ProjectConfig;
use cargo_generate::{generate, GenerateArgs, TemplatePath};
use std::collections::HashMap;
use std::error::Error;
use std::path::PathBuf;

pub fn generate_project(config: &ProjectConfig, destination: &PathBuf) -> Result<(), Box<dyn Error>> {
    println!("\n⚙️ Preparing project generation...");
    let mut template_variables = HashMap::<String, String>::new();

    template_variables.insert("project_name".into(), config.project_name.clone());
    template_variables.insert("author_name".into(), config.author_name.clone());
    template_variables.insert("author_email".into(), config.author_email.clone());
    template_variables.insert("app_identifier".into(), config.app_identifier.clone());
    template_variables.insert("include_server".into(), config.include_server.to_string());
    template_variables.insert("include_frontend".into(), config.include_frontend.to_string());
    template_variables.insert("include_tauri_desktop".into(), config.include_tauri_desktop.to_string());

    if let Some(db_name) = &config.db_name { template_variables.insert("db_name".into(), db_name.clone()); }
    if let Some(db_admin) = &config.db_owner_admin { template_variables.insert("db_owner_admin".into(), db_admin.clone()); }
    if let Some(db_pword) = &config.db_owner_pword { template_variables.insert("db_owner_pword".into(), db_pword.clone()); }

    let gen_args = GenerateArgs {
        overwrite: true,
        template_path: TemplatePath {
            git: Some("https://github.com/Yrrrrrf/gwa.git".to_string()),
            branch: Some("templatize-dev".to_string()),
            ..Default::default()
        },
        name: Some(config.project_name.clone()),
        destination: Some(destination.clone()),
        define: template_variables.into_iter().map(|(k, v)| format!("{}={}", k, v)).collect(),
        verbose: true,
        ..Default::default()
    };

    println!("🚀 Generating project... this may take a moment.");
    match generate(gen_args) {
        Ok(output_path) => {
            println!("\n✅ GWA project '{}' created successfully!", config.project_name);
            println!("   Location: {}", output_path.to_string_lossy());
            println!("\nNext steps:");
            println!("   cd {}", config.project_name);
            println!("   Follow the instructions in the new README.md to get started.");
        }
        Err(e) => {
            eprintln!("\n❌ Error generating project: {}", e);
            return Err(e.into());
        }
    }

    Ok(())
}