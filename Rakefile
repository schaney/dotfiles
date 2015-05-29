DONT_LINK = ["Rakefile", "README.markdown"]

task :default => :link

desc "Symlinks the dotfiles to #{ENV['HOME']}"
task :link do
  puts files
  files.each do |p|
    link = File.expand_path "~/.#{File.basename(p)}"
    run %Q{ln -s "#{p}" "#{link}"} unless File.exists?(link)
  end
end

desc "Removes all symlinks to dotfiles from #{ENV['HOME']}"
task :unlink do
  files.each do |p|
    link = File.expand_path "~/.#{File.basename(p)}"
    run %Q{rm "#{link}"}
  end
end

def pwd
  File.expand_path(File.dirname(__FILE__))
end

def files
  Dir["/Users/sean/.dotfiles/*"].reject { |p| DONT_LINK.include?(File.basename(p)) }
end
 
def run(cmd)
  puts cmd
  system cmd
end
