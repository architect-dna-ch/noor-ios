require 'spaceship'

Spaceship::Portal.login('systems@architect-dna.ch')
Spaceship::Portal.select_team

bundle_id = 'ch.architectdna.voidfreq'
out = '/Users/besonnet.kl2/void-freq-ios/signing/VoidFreq_fresh.mobileprovision'

# Find existing distribution cert
cert = Spaceship::Portal::Certificate::Production.all.first
puts "Using cert: #{cert.id} expires #{cert.expires}"

# Revoke any old profiles with same name and recreate
Spaceship::Portal::ProvisioningProfile::AppStore.all.each do |p|
  if p.name == 'VoidFreq Distribution'
    puts "Revoking old profile: #{p.id}"
    p.delete!
  end
end

profile = Spaceship::Portal::ProvisioningProfile::AppStore.create!(
  bundle_id: bundle_id,
  certificate: cert,
  name: 'VoidFreq Distribution'
)

data = profile.download
File.write(out, data)
puts "Profile UUID: #{profile.uuid}"
puts "Saved to: #{out}"
puts "File size: #{File.size(out)} bytes"
