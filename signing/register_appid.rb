require 'spaceship'

Spaceship::Portal.login('systems@architect-dna.ch')
Spaceship::Portal.select_team

bundle_id = 'ch.architectdna.voidfreq'

existing = Spaceship::Portal::App.find(bundle_id)
if existing
  puts "App ID already exists: #{existing.app_id} — #{existing.name}"
else
  app = Spaceship::Portal::App.create!(
    bundle_id: bundle_id,
    name: 'VOID FREQ'
  )
  puts "Created App ID: #{app.app_id}"
end
