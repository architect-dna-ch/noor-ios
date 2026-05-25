require 'spaceship'

username = 'systems@architect-dna.ch'
bundle_id = 'ch.architectdna.voidfreq'
csr_path = File.join(__dir__, 'distribution.csr')
output_dir = __dir__

puts "Logging in..."
Spaceship::Portal.login(username)
Spaceship::Portal.select_team

puts "Creating distribution certificate..."
csr_content = File.read(csr_path)
cert = Spaceship::Portal::Certificate::Production.create!(csr: csr_content)
puts "Certificate created: #{cert.id}"

cert_path = File.join(output_dir, "distribution.cer")
File.write(cert_path, cert.download)
puts "Certificate downloaded → #{cert_path}"

puts "Creating provisioning profile..."
profile = Spaceship::Portal::ProvisioningProfile::AppStore.create!(
  bundle_id: bundle_id,
  certificate: cert,
  name: 'VoidFreq Distribution'
)

profile_path = File.join(output_dir, "VoidFreq.mobileprovision")
File.write(profile_path, profile.download)
puts "Profile downloaded → #{profile_path}"

puts "\nDone ✓"
puts "  Cert:    #{cert_path}"
puts "  Profile: #{profile_path}"
